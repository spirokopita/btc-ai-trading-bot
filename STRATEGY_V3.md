# Strategy V3 — Predict net result, not gross 48-hour Bitcoin rise

## Status
**Research / paper only. NOT a validated profitable trading system.** We have deliberately not activated live trades. Prior V2 proxy tests: AI rejected all 79 setups; technical-only lost approximately 4.6% of the whole simulated account over Jan 2023–Sep 2026. A preliminary V3 *technical-only* replay (without the AI) still lost 3.9% over that period. **No end-to-end V3 FreqAI backtest has passed.**

## What changed from V2

| Parameter | V2 | V3 research candidate |
|---|---|---|
| AI prediction target | 48-hour gross price change | Next-open initiated trade **net P&L**, including simulated fees, slippage, stop, target, and maximum hold |
| AI decision condition | Gross gain > max(3.3%, fees + ATR factor) | Predicted average **net P&L > +1.2%**, on valid data. No forced entries if unproven. |
| Holding duration | 72–120h | 12 days / 72 four-hour bars |
| Loss stop | -3.5% price | -4.5% price (about -6.4% realised net after costs; worse on gaps) |
| Take profit | +4.5% trade net profit | +5.5% trade net profit (approx +7.5% price in label, not exact) |
| Entry filter | EMA20 crossover, RSI 50-68, ADX18 | Pullback within last 4 candles, close > EMA20, RSI 40-68, ADX14 |
| Retraining | 24h | 7 days |
| Training history | 60 days | 365 days (REQUIRES ARCHIVE; cannot bootstrap from 720-candle exchange OHLC limit) |
| Max trade allocation | 5% | 5%, one position |
| Daily / cumulative lockouts | -2% daily, -5% high-water mark, -10% initial | Same independent guard |

## Fixed assumptions

- Market: Kraken BTC/AUD spot, 4h, market entry/exit, no leverage, no shorts.
- Gross barriers used in training: +7.5% take, -4.5% stop, 72 four-hour bars maximum. **Intrabar ambiguous bars are scored as stop first.** Open gaps worsen fills; simulated slippage is 0.2% on each side.
- Kraken Tier-1 fees assumed 0.8% taker entry and 0.8% taker exit; modeled total 2.0% round-trip impact before market moves. Fee rates must be checked at the time of live activation.
- The label uses **next bar OPEN** as hypothetical purchase, not the currently observed CLOSE. Last 72 candles have no valid target and cannot be used as mature labels. Labels reference future data strictly for supervised training, never as model features.
- `stoploss=-0.045` and `minimal_roi={'0': 0.055}` are Freqtrade's operational rules, which may differ slightly from the gross OHLC barrier used in training because true trade fees, spread and fill timing vary. This **train/execution mismatch requires integration testing**; no claim of exact parity.
- Model estimate is expected NET P&L, not a guarantee. Any threshold must be validated on separate market periods and rechecked for calibration/drift.

## Signal logic

Positive EMA200 slope over 12 bars; close above EMA200; EMA50 above EMA200; ADX >= 14; close above EMA20; minimum recent 4-candle low touches EMA20 (within 0.5%); no chase higher than 1.25 ATR from EMA20; RSI14 40–68; ATR14 0.5–7% of price; volume >= 50% rolling average. FreqAI `do_predict == 1` and estimated next-open net trade return 1.2–20%. All other situations HOLD AUD.

## Live and safety

The independent watchdog blocks new entries if stale, out of sync or equity limits are breached. Its stop is sticky. The account risk controls cannot guarantee maximum losses. Protective exchange-side stop-market orders must be tested on Kraken with a tiny position; a 12-day time exit requires the bot to be running. Use trade-only API permissions with no withdrawal or transfer scope. Secrets are NOT provided by setup script.

## Validation requirements

1. Assemble multi-year **Kraken BTC/AUD** OHLCVT 4h archives, including updates to the requested date; never fill missing bars by inventing prices. Kraken publishes ZIPs: <https://support.kraken.com/au/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data>.
2. Train chronologically with a 72-bar gap/label maturity embargo. Use 2021–2023 as initial learning period, 2024 for development, and report 2025–2026 as *diagnostic only* because prior analysis has already considered some of those years. Reserve the next untouched forward period for genuine proof.
3. Compare AI vs the *same* technical rule set without AI, buy-and-hold, and AUD cash; use identical trade sizing/execution assumptions. Report net expectancy per trade, per-year returns, maximum drawdown, time invested, number of trades, and losses due to fees. Run high-slippage stress scenarios.
4. Make zero-trade models a FAIL TO DEMONSTRATE EDGE, not a success. Do not tune thresholds just to force activity.
5. Run Freqtrade lookahead-analysis, multiple rolling backtests, and 30–60+ days of dry-run trading. No automatic progression to live mode. Change only one predeclared parameter at a time, and log each experiment.
6. Live integration is unverified here: exchange-specific stop behaviour, FreqAI train/label compatibility and actual fills require server-side testing.
