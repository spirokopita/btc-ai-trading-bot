"""Read-only snapshots of V5/V7/V10/V11 databases, never creates or edits DBs.

Facts are anchored to the last persisted candle and heartbeat. In particular,
market source strings are provenance *labels*, not independent verification.
Wallet equity on a candle is an estimated after-exit-fees liquidation value.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sqlite3
import time
from trading_costs import FeeTier, FeeSettings, estimate_execution


@dataclass(frozen=True)
class DashboardSources:
    market: Path = Path('data/market.sqlite')
    wallet: Path = Path('data/loop_wallet.sqlite')
    news: Path = Path('data/news.sqlite')
    journal: Path = Path('data/loop_journal.sqlite')


def _ro(path: Path):
    """Open an existing file with SQLite mode=ro; no creation and no WAL writes."""
    if not path.is_file():
        return None
    db=sqlite3.connect(path.resolve().as_uri()+'?mode=ro', uri=True, timeout=2)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    return db


def _safe_number(value):
    number=float(value)
    return number if math.isfinite(number) else None


def _row(row):
    return dict(row) if row else None


def _unpack_wallet(db, now):
    wallet=_row(db.execute('SELECT * FROM wallet WHERE id=1').fetchone())
    if wallet is None:
        return None
    config=_row(db.execute('SELECT * FROM config WHERE id=1').fetchone())
    if config is None:
        raise ValueError('Wallet config missing')
    f=json.loads(config['fee_json']);f['tiers']=tuple(FeeTier(**v) for v in f['tiers'])
    settings=FeeSettings(**f)
    pos=_row(db.execute('SELECT * FROM position WHERE id=1').fetchone())
    totals=_row(db.execute('''SELECT COUNT(*) as closed_trades,
        COALESCE(SUM(CASE WHEN net_pnl_quote>0 THEN 1 ELSE 0 END),0) as winners,
        COALESCE(SUM(gross_pnl_quote),0) as realized_gross_quote,
        COALESCE(SUM(net_pnl_quote),0) as realized_net_quote,
        COALESCE(SUM(fees_quote),0) as trading_fees_quote,
        COALESCE(SUM(spread_quote),0) as spread_quote,
        COALESCE(SUM(slippage_quote),0) as slippage_quote
        FROM trades''').fetchone())
    open_pos=None;liquidation=0.;unrealized=None
    if pos:
        mark=wallet['last_close']
        if mark is not None:
            estimated=estimate_execution(mark,pos['quantity'],'sell','taker',settings,wallet['last_volatility'])
            liquidation=estimated.executed_notional_quote-estimated.fee_quote
            unrealized=liquidation-pos['entry_outlay']
        open_pos={'quantity_btc':pos['quantity'],'entry_ts':pos['entry_ts'],
                  'entry_mid_quote':pos['entry_mid'],'entry_outlay_quote':pos['entry_outlay'],
                  'stop_mid_quote':pos['stop_mid'],'target_mid_quote':pos['target_mid'],
                  'estimated_liquidation_quote':liquidation if mark is not None else None,
                  'estimated_unrealized_net_quote':unrealized,
                  'candle_based_estimate':True}
    initial=wallet['initial_cash'];cash=wallet['cash']
    equity=cash+liquidation if not pos or wallet['last_close'] is not None else None
    assert equity is None or math.isclose(cash+liquidation,equity,abs_tol=1e-8)
    # The wallet cash flows must reconcile exactly with all completed trades.
    expected_cash=initial+totals['realized_net_quote']-(pos['entry_outlay'] if pos else 0)
    if not math.isclose(cash,expected_cash,rel_tol=1e-9,abs_tol=1e-6):
        raise ValueError('Wallet cash/trade reconciliation failed')
    recent=[]
    for item in db.execute('''SELECT id,entry_ts,exit_ts,exit_reason,quantity,
      gross_pnl_quote,fees_quote,spread_quote,slippage_quote,net_pnl_quote,
      ledger_json FROM trades ORDER BY id DESC LIMIT 20'''):
        row=dict(item)
        details=json.loads(row.pop('ledger_json'))
        row['entry_fee_quote']=details.get('entry_fee_quote')
        row['exit_fee_quote']=details.get('exit_fee_quote')
        if not math.isclose(row['gross_pnl_quote']-row['fees_quote']-row['spread_quote']-row['slippage_quote'],row['net_pnl_quote'],abs_tol=1e-6):
            raise ValueError('Closed trade gross-to-net reconciliation failed')
        recent.append(row)
    orders=[dict(row) for row in db.execute('''SELECT id,client_id,side,kind,status,
        submitted_after_ts,filled_ts,limit_mid,budget_quote,reason
        FROM orders ORDER BY id DESC LIMIT 20''')]
    curve=[dict(row) for row in db.execute('''SELECT ts,cash,exit_value,equity_net,halted_reason
        FROM equity_snapshots ORDER BY ts DESC LIMIT 300''')][::-1]
    realized=totals['realized_net_quote']
    return {'mode':'PAPER_ONLY','pair':'BTC/AUD','quote_currency':'AUD',
            'interval_minutes':config['interval'],'last_candle_ts':wallet['last_ts'],
            'last_mid_quote':wallet['last_close'], 'initial_quote':initial,
            'cash_quote':cash,'equity_net_quote':equity,
            'total_estimated_net_quote':equity-initial if equity is not None else None,
            'realized_net_quote':realized,'estimated_unrealized_net_quote':unrealized,
            'realized_gross_quote':totals['realized_gross_quote'],
            'trading_fees_quote':totals['trading_fees_quote'],
            'spread_quote':totals['spread_quote'],'slippage_quote':totals['slippage_quote'],
            'total_costs_quote':totals['trading_fees_quote']+totals['spread_quote']+totals['slippage_quote'],
            'closed_trades':totals['closed_trades'],'winners':totals['winners'],
            'win_rate_pct':100*totals['winners']/totals['closed_trades'] if totals['closed_trades'] else None,
            'risk_halt':wallet['halted_reason'],'high_water_quote':wallet['high_water'],
            'position':open_pos,'orders':orders,'trades':recent,'equity_curve':curve}


def _market(db):
    rows=[dict(x) for x in db.execute('''SELECT interval,COUNT(*) candle_count,MIN(ts) first_ts,
            MAX(ts) last_ts,COUNT(DISTINCT source) source_count
            FROM candles WHERE exchange='kraken' AND pair='BTC/AUD'
            GROUP BY interval ORDER BY interval''')]
    for r in rows:
        newest=db.execute('''SELECT source FROM candles WHERE exchange='kraken' AND pair='BTC/AUD'
            AND interval=? ORDER BY ts DESC LIMIT 1''',(r['interval'],)).fetchone()
        r['latest_source_label']=newest['source'] if newest else None
        # Keep 15-second dashboard polls cheap on multi-year 1m data.
        # The last 2000 observed bars are inspected; this is NOT full-history QC.
        recent=[x['ts'] for x in db.execute('''SELECT ts FROM candles
          WHERE exchange='kraken' AND pair='BTC/AUD' AND interval=?
          ORDER BY ts DESC LIMIT 2000''',(r['interval'],))]
        r['gap_sample_candles']=len(recent)
        r['missing_interval_count']=sum(max(0,(a-b)//(r['interval']*60)-1)
             for a,b in zip(recent, recent[1:]))
    return rows


def _news(db):
    items=[]
    for row in db.execute('''SELECT id,source,headline,available_ts,first_seen_ts,published_ts,
      categories_json,assets_json,polarity,polarity_label FROM news
      ORDER BY available_ts DESC,id DESC LIMIT 25'''):
        x=dict(row);x['categories']=json.loads(x.pop('categories_json'))
        x['assets']=json.loads(x.pop('assets_json'));items.append(x)
    feeds=[dict(x) for x in db.execute('''SELECT feed,last_attempt_ts,last_success_ts,last_error
         FROM feed_state ORDER BY feed LIMIT 30''')]
    return {'articles':items,'feed_states':feeds}


def _journal(db):
    health=[dict(x) for x in db.execute('''SELECT observed_at,status,details FROM health
        ORDER BY id DESC LIMIT 20''')]
    decisions=[]
    for row in db.execute('''SELECT candle_ts,decision,reason,evidence_json,recorded_at
      FROM decisions ORDER BY candle_ts DESC LIMIT 25'''):
        x=dict(row);x['evidence']=json.loads(x.pop('evidence_json'));decisions.append(x)
    return {'health':health,'decisions':decisions}


def read_snapshot(sources: DashboardSources, *, now: int|None=None) -> dict:
    """Single current read per DB, fail closed for missing/corrupt components.

    Exposing incomplete state is better than silently converting missing data
    into cash, a zero P&L, or healthy status.
    """
    now=int(time.time()) if now is None else int(now)
    result={'generated_at_utc':now,'mode':'PAPER_ONLY','real_orders':0,
            'account':None,'market':[],'news':None,'journal':None,
            'warnings':[],'read_only':True,'historical_profitability_verified':False}
    tasks=[('account',sources.wallet,_unpack_wallet),('market',sources.market,_market),
           ('news',sources.news,_news),('journal',sources.journal,_journal)]
    for key,path,load in tasks:
        try:
            db=_ro(Path(path))
            if db is None:
                result['warnings'].append(f'{key}: database not found; no observations available')
                continue
            try:
                db.execute('BEGIN')  # transaction snapshot; query_only protects it
                result[key]=load(db,now) if key=='account' else load(db)
                db.execute('ROLLBACK')  # close the read transaction without mutation
            finally:db.close()
        except (sqlite3.Error,ValueError,TypeError,KeyError,OverflowError) as exc:
            result[key]=None if key!='market' else []
            result['warnings'].append(f'{key}: unavailable or inconsistent ({type(exc).__name__})')
    acct=result['account']
    if acct is None:
        result['warnings'].append('Paper wallet uninitialised or unreadable; no account P&L available')
    else:
        if acct['risk_halt']:
            result['warnings'].append('Paper wallet risk lock ACTIVE: '+acct['risk_halt'])
        if acct['last_candle_ts'] is None:
            result['warnings'].append('Wallet has no priced candles; equity is not a current market valuation')
        else:
            interval=acct['interval_minutes']*60
            age=now-(acct['last_candle_ts']+interval)
            if age>2*interval:
                result['warnings'].append('Wallet price is stale (last processed candle closed more than two periods ago)')
    if not result['market']:
        result['warnings'].append('No cached BTC/AUD market candles. Historical Kraken P&L has NOT been measured')
    elif any(r['missing_interval_count'] for r in result['market']):
        result['warnings'].append('Recent market candle gaps detected (last 2,000 candles per timeframe); no values are interpolated')
    if any('SYNTHETIC' in (r['latest_source_label'] or '').upper() for r in result['market']):
        result['warnings'].append('Synthetic fixture candle source present: prices must not be reported as genuine Kraken history')
    if result['journal'] is None or not result['journal']['health']:
        result['warnings'].append('No loop heartbeat observed; service status UNKNOWN')
    else:
        last=result['journal']['health'][0]
        if now-last['observed_at']>1800:
            result['warnings'].append('Last loop heartbeat older than 30 minutes; daemon may be OFFLINE')
        if last['status'].upper() not in ('OK','HEALTHY'):
            result['warnings'].append('Loop reported '+last['status'])
    if result['news'] is None or not result['news']['articles']:
        result['warnings'].append('No news observations; news signal coverage unavailable')
    return result
