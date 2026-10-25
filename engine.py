"""Unified historical replay using the actual V7 PaperEngine for every fill.

No broker/network code, no future-candle signal leakage. This is a *technical*
control strategy; it is not an AI forecast. Fees-on and fees-off both use the
identical signal policy and identical risk settings, in separate wallets.
OHLC intrabar order sequencing and spread/impact estimates are approximations.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable

from data_layer.storage import Candle, validate, CandleStore
from paper_engine import PaperEngine, RiskLimits
from trading_costs import FeeSettings, load_settings


@dataclass(frozen=True)
class BacktestParameters:
    interval: int = 240
    breakout_bars: int = 120       # 20 days of 4h candles
    exit_low_bars: int = 60        # 10 days of 4h candles
    fast_ema_bars: int = 50
    slow_ema_bars: int = 200
    stop_pct: float = 0.10
    target_pct: float = 9.0        # inert high target: breakout uses channel exits
    cooldown_bars: int = 12

    @classmethod
    def for_interval(cls, interval: int):
        """Preserve 20-day/10-day and 4h-EMA equivalent lookbacks at other resolutions."""
        if interval not in (1, 5, 15, 30, 60, 240, 720, 1440):
            raise ValueError('Unsupported interval')
        return cls(interval=interval,
                   breakout_bars=20*24*60//interval,
                   exit_low_bars=10*24*60//interval,
                   fast_ema_bars=max(2,round(50*240/interval)),
                   slow_ema_bars=max(2,round(200*240/interval)),
                   cooldown_bars=max(1,round(12*240/interval)))

    def __post_init__(self):
        if self.interval not in (1, 5, 15, 30, 60, 240, 720, 1440):
            raise ValueError('Unsupported interval')
        if any(not isinstance(getattr(self, a), int) or getattr(self, a) < 1
               for a in ('breakout_bars','exit_low_bars','fast_ema_bars',
                         'slow_ema_bars')):
            raise ValueError('Lookbacks must be positive integers')
        if not isinstance(self.cooldown_bars, int) or self.cooldown_bars < 0:
            raise ValueError('Invalid cooldown_bars')
        if not (0 < self.stop_pct < 1 and 0 < self.target_pct <= 10):
            raise ValueError('Invalid stop/target')


class DonchianBreakout:
    """Pure causal close-of-bar signals; prior lookbacks EXCLUDE current candle."""
    def __init__(self, params: BacktestParameters):
        self.p=params
        self.highs=[]
        self.lows=[]
        self.e_fast=None
        self.e_slow=None
        self.count=0

    def observe(self, candle: Candle) -> tuple[bool,bool]:
        p=self.p
        prior_hi=max(self.highs[-p.breakout_bars:]) if len(self.highs)>=p.breakout_bars else None
        prior_lo=min(self.lows[-p.exit_low_bars:]) if len(self.lows)>=p.exit_low_bars else None
        self.e_fast=(candle.close if self.e_fast is None else
                     self.e_fast+(2/(p.fast_ema_bars+1))*(candle.close-self.e_fast))
        self.e_slow=(candle.close if self.e_slow is None else
                     self.e_slow+(2/(p.slow_ema_bars+1))*(candle.close-self.e_slow))
        self.count+=1
        # These are independent signals. The runner decides depending on open position.
        warm=self.count>=max(p.breakout_bars+1,p.exit_low_bars+1,
                             p.fast_ema_bars,p.slow_ema_bars)
        buy=bool(warm and prior_hi is not None and candle.volume>0 and
                 candle.close>prior_hi and candle.close>self.e_slow and
                 self.e_fast>self.e_slow)
        sell=bool(warm and prior_lo is not None and
                  (candle.close<prior_lo or candle.close<self.e_slow))
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        # Prevent unbounded memory in always-on testing.
        cap=max(p.breakout_bars,p.exit_low_bars)
        if len(self.highs)>cap: self.highs.pop(0);self.lows.pop(0)
        return buy,sell


def checked_candles(candles: Iterable[Candle], interval: int) -> list[Candle]:
    """Fail closed on missing, shuffled, duplicate or invalid bars."""
    bars=list(candles)
    if not bars:
        raise ValueError('No OHLCV candles supplied; import genuine BTC/AUD first')
    step=interval*60
    previous=None
    for candle in bars:
        validate(candle,interval)
        if previous is not None and candle.ts-previous!=step:
            raise ValueError(f'Non-contiguous candles: expected {previous+step}, got {candle.ts}; '
                             'do not fabricate missing market prices')
        previous=candle.ts
    return bars


def _scalar_float(v, label):
    v=float(v)
    if not math.isfinite(v):raise ArithmeticError(f'Non-finite metric {label}')
    return v


def metrics_from_wallet(wallet: PaperEngine, *, count: int, interval: int) -> dict:
    """Risk/return computed from liquidatable equity after fees, at EACH bar close.

    Sharpe is annualized sample mean/std of equally spaced bar returns, zero
    risk-free rate, 365-day crypto year. A zero-volatility return stream gets
    Sharpe=null instead of a fabricated infinity.
    """
    snapshots=wallet.db.execute('SELECT ts,equity_net FROM equity_snapshots ORDER BY ts').fetchall()
    if len(snapshots)!=count or count<1:raise ValueError('Incomplete equity snapshot series')
    values=[float(wallet.risk.starting_cash)]+[float(x['equity_net']) for x in snapshots]
    for v in values:_scalar_float(v,'equity')
    returns=[values[i]/values[i-1]-1 for i in range(1,len(values))]
    if any(v<=0 for v in values):raise ArithmeticError('Negative equity in spot paper account')
    peak=values[0]
    max_dd=0.0
    for value in values[1:]:
        peak=max(value,peak)
        max_dd=min(max_dd,value/peak-1)
    sharpe=(mean(returns)/stdev(returns)*math.sqrt(365*1440/interval)
            if len(returns)>=2 and stdev(returns)>1e-15 else None)
    ledgers=wallet.trades()
    pnl=[float(t['net_pnl_quote']) for t in ledgers]
    positive=sum(p for p in pnl if p>0)
    negative=-sum(p for p in pnl if p<0)
    profit_factor=(positive/negative if negative>1e-12 else
                   ('Infinity' if positive>1e-12 else None))
    gross_positive=sum(max(float(t['gross_pnl_quote']),0.) for t in ledgers)
    fees=sum(float(t['total_trading_fees_quote']) for t in ledgers)
    spread=sum(float(t['spread_quote']) for t in ledgers)
    slippage=sum(float(t['slippage_quote']) for t in ledgers)
    gross=sum(float(t['gross_pnl_quote']) for t in ledgers)
    net=sum(pnl)
    audit=wallet.verify()
    if not math.isclose(net,gross-fees-spread-slippage,abs_tol=1e-6):
        raise ArithmeticError('Backtest aggregate gross-to-net ledger mismatch')
    state=wallet.status()
    return {
      'mode':'PAPER_ONLY', 'account_initial_quote':values[0],
      'account_final_liquidation_quote':values[-1],
      'total_return_net_pct':100*(values[-1]/values[0]-1),
      'realized_net_pnl_quote':net,
      'unrealized_liquidation_pnl_quote':values[-1]-values[0]-net,
      'gross_realized_pnl_quote':gross,
      'total_trading_fees_quote':fees,'total_spread_quote':spread,
      'total_slippage_quote':slippage,'total_explicit_and_implicit_costs_quote':fees+spread+slippage,
      'fees_pct_of_gross_winning_trade_profit':100*fees/gross_positive if gross_positive>0 else None,
      'net_win_rate_pct':100*sum(p>0 for p in pnl)/len(pnl) if pnl else None,
      'net_profit_factor':profit_factor,
      'max_drawdown_pct':100*max_dd,
      'annualized_sharpe_zero_riskfree':sharpe,
      'completed_trades':len(ledgers),'wins_net':sum(p>0 for p in pnl),
      'losses_net':sum(p<0 for p in pnl),
      'open_position':state['position'] is not None,
      'halt_reason':state['halt_reason'],
      'candles_processed':count,'verification':audit,
      'equity_curve':[{'ts':row['ts'],'equity_net_quote':row['equity_net']} for row in snapshots],
      'trades':ledgers,
    }


def run_backtest(candles: Iterable[Candle], db_path: str | Path,
                 *, settings: FeeSettings | None = None,
                 risk: RiskLimits | None = None,
                 params: BacktestParameters | None = None,
                 trade_after_ts: int | None = None) -> dict:
    params=params or BacktestParameters()
    bars=checked_candles(candles,params.interval)
    path=Path(db_path)
    if path.exists():raise FileExistsError('Historical replay requires a fresh wallet DB')
    risk=risk or RiskLimits()
    settings=settings or load_settings()
    strategy=DonchianBreakout(params)
    step=params.interval*60
    last_close=None
    atr_est=None
    last_exit_ts=-10**20
    with PaperEngine(path,settings=settings,risk=risk,interval=params.interval) as wallet:
        for candle in bars:
            # The estimate visible at this opening comes from PREVIOUS closed bars.
            # Never use this bar's high/low to improve its own order fills.
            causal_atr=(atr_est/last_close if atr_est is not None and
                        last_close is not None else 0.0)
            wallet.on_candle(candle, volatility_frac=min(1.0,causal_atr))
            tr=(candle.high-candle.low if last_close is None else
                max(candle.high-candle.low,abs(candle.high-last_close),
                    abs(candle.low-last_close)))
            atr_est=(tr if atr_est is None else (atr_est*13+tr)/14)
            last_close=candle.close
            # A protective or discretionary exit can happen on this candle. Do not
            # enter again on its closing signal; enforce a historical cooldown.
            latest=wallet.db.execute('SELECT exit_ts FROM trades ORDER BY id DESC LIMIT 1').fetchone()
            if latest:last_exit_ts=latest['exit_ts']
            buy,sell=strategy.observe(candle)
            if trade_after_ts is not None and candle.ts < trade_after_ts:
                continue  # warm-up only: indicators update, wallet cannot trade
            state=wallet.status()
            if state['halt_reason']:continue
            if state['position'] is not None:
                if sell and not state['pending']:
                    wallet.place_sell(kind='market',client_id=f'exit-{candle.ts}')
            elif buy and candle.ts-last_exit_ts>params.cooldown_bars*step and not state['pending']:
                stake=min(risk.max_order_quote,
                          risk.max_position_fraction*state['equity_net_quote'],
                          state['cash_quote'])
                # Floating point position cap makes it safer to avoid exact boundary.
                stake*=1-1e-10
                if stake>=risk.min_order_quote:
                    wallet.place_buy(stake,stop_pct=params.stop_pct,target_pct=params.target_pct,
                                     client_id=f'entry-{candle.ts}')
        out=metrics_from_wallet(wallet,count=len(bars),interval=params.interval)
        out['paper_wallet_sqlite']=str(path)
        return out


def compare_costs(candles: Iterable[Candle], out_dir: str | Path,
                  *, settings: FeeSettings | None = None,
                  risk: RiskLimits | None = None,
                  params: BacktestParameters | None = None) -> dict:
    params=params or BacktestParameters()
    bars=checked_candles(candles,params.interval)
    out=Path(out_dir)
    out.mkdir(parents=True,exist_ok=True)
    if (out/'costs_on.sqlite').exists() or (out/'costs_off.sqlite').exists():
        raise FileExistsError('Cost-comparison output already exists; use a new directory')
    active=run_backtest(bars,out/'costs_on.sqlite',settings=settings or load_settings(),risk=risk,params=params)
    control=run_backtest(bars,out/'costs_off.sqlite',settings=FeeSettings.zero(),risk=risk,params=params)
    return {'dataset':'user supplied; provenance in source report',
            'assumptions':'OHLC bar replay; trade-through maker fills not guaranteed',
            'fee_on':active,'fee_off':control,
            'difference_fee_on_minus_off_return_percentage_points':
                active['total_return_net_pct']-control['total_return_net_pct']}


def candles_from_store(path: str | Path, interval: int=240,
                      start: int | None=None,end: int | None=None) -> tuple[list[Candle],dict]:
    with CandleStore(path) as db:
        src=db.candles('kraken','BTC/AUD',interval,start,end)
    bars=[Candle(row['ts'],row['o'],row['h'],row['l'],row['c'],row['v'],row['trades']) for row in src]
    provenance=sorted({row['source'] for row in src})
    return bars,{'exchange_claim_in_store':'kraken','pair':'BTC/AUD',
                 'interval_minutes':interval,'sources_in_database':provenance,
                 'observations':len(bars),'verified_exchange_provenance':False}
