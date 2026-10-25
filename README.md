# V13 — Android-first BTC/AUD paper-monitor project

**New:** [`android/README.md`](android/README.md) explains the native Kotlin project, A$1,000 simulated prefill/refill/reset, purple notification, two home-screen widgets, public market monitor and honest APK build status. The existing Python V12 strategy/fee/wallet/backtester code remains intact and regression-tested. **No real wallet, trading keys, or live trading.**

**Build blocker:** No Android SDK/Gradle in this execution environment. Source delivered; **not** an APK or tested phone app. Latest changelog: [`CHANGELOG.md`](CHANGELOG.md).

---

# V12 — Read-only Paper Trading Dashboard (Roadmap 8)

**Paper trading only.** The dashboard cannot buy, sell, cancel, initialise wallets,
modify strategies or contact private Kraken APIs. It exposes a local GET-only
interface, default binding **127.0.0.1:8787**, without external JavaScript
libraries, logins, writable endpoints or API keys.

Run from the V12 project directory (Python 3.11+):

```bash
python3 -m unittest discover -s tests -q
python3 -m dashboard.server --port 8787
# Visit http://127.0.0.1:8787 from the SAME computer.
# Start the V11 paper loop separately; the dashboard never starts the bot.
python3 -m strategy_loop.cli serve --poll-seconds 60 --sync-seconds 900
```

Use `--market-db`, `--wallet-db`, `--news-db` and `--journal-db` when your
paper worker uses other locations. The defaults match V11's loop databases.
For remote access use **an authenticated SSH tunnel** (or VPN and controlled
reverse proxy), leaving the dashboard bound to local loopback. **Never bind
0.0.0.0** or forward the unauthenticated monitor directly onto the internet.

The black-and-white adaptive monitor refreshes every 15 seconds: estimated
NET liquidation equity, realized net/gross trade P&L, actual modeled maker/taker
fee totals, spread, slippage, open position and protective levels, latest
simulated orders, ledger trades, history coverage/gaps, first-seen news and
news-category evidence in decisions, health/error journal and warnings. The
historical source displayed is a provenance **label**, not independent source
authentication. Market gaps on dashboard are counted over the last 2,000
candles per timeframe for responsive polling; use the V5 full-database gap
report for complete coverage. Net liquidation equity is estimated at the
**last completed candle** and includes estimated sell-side friction; it is
**not** a real-time wallet balance or exchange valuation.

If an input SQLite database is missing, corrupt, stale or inconsistent, the
UI explicitly flags it. The packaged BTC/AUD market database contains **zero
verified genuine candles**, and the default paper loop wallet/news/health DBs
are absent: the dashboard therefore shows UNKNOWN/NO DATA, **not zero
historical profit**. For a deterministic local accounting example run
`python3 -m examples.dashboard_demo` — those prices are completely synthetic
and never written to the authentic market cache. The sample report is in
`reports/dashboard_synthetic_demo.json`.

---

## V11 / Roadmap 7 — autonomous **PAPER-ONLY** BTC/AUD decision loop (2026-10-24)

**No exchange orders are sent.** The new `strategy_loop/` combines prior
4h-candle Donchian/EMA breakout indicators with point-in-time validated news
observations and a strict `trading_costs` *net-after-fee* edge gate. V7 wallet
executes all orders **in SQLite only**, after the following candle becomes
available. It does NOT contain live broker order methods or embedded keys.

**What the always-running service does**

1. Polls Kraken's public, no-key OHLC endpoint and the V10 HTTPS RSS feeds;
   records request errors and backs off (status `serve`). Candle gaps or old
   data cause a fail-closed error; any failed source blocks **new entries**.
2. Reconstructs the 20-day breakout signal from actual completed bars on
   restart. Backfilled historical bars only warm the model and settle prior
   **simulated** orders; it cannot create retroactive entry signals.
3. Requires a current breakout, a recently *actually observed* BTC/market/macro
   positive article, enough previously matured news-event samples in
   chronological train + purged holdout, and a **positive after-fee expected
   move** exceeding a configurable 0.5% additional net edge. Without credible
   news-based edge evidence, it simply **HOLDS**. News is an imperfect
   association, not a causal predictor or independently proven profitable AI.
4. Defaults to an improved-price **maker-limit** order 0.10% below the last
   close, cancelled after 3 bars without strict trade-through; no market order
   chasing. A taker option is available in Python config but never changes
   the wallet into live execution. The V6 cost gate uses the selected
   maker/taker assumptions, both entry and exit fees, spread and slippage.
5. Enforces V7 risk limits, protective stops and exits even if news/network
   collection fails. One-process `fcntl` lock, predictable order client IDs,
   persistent candle/decision log and a health journal make repeated calls
   safe. Host OS/systemd handles OS restarts; deployment is not installed here.

### Local commands

```bash
# Empty real BTC/AUD cache? This MUST report failure rather than invent prices:
python3 -m strategy_loop.cli once --no-network

# After IMPORTING genuine, gap-audited Kraken BTC/AUD candles and building
# actual first-observed RSS history on a network-connected Linux host:
python3 -m strategy_loop.cli once
python3 -m strategy_loop.cli serve --poll-seconds 60 --sync-seconds 900
python3 -m strategy_loop.cli status

# Offline synthetic accounting / idempotency demo (NO Bitcoin market data):
python3 -m examples.strategy_loop_demo
python3 -m unittest discover -s tests -q
```

`serve` polls the *public* Kraken and news endpoints on schedule, and never
places actual orders. It must run on a continuously connected machine with
Python dependencies installed. `deploy/crypto-paper-bot.service.example` is a
systemd template; adjust account and paths before deploying, and never enable
private exchange trading keys. The template has **not** been installed here.

**Provenance and real-world caveats:** Source names inside SQLite are claims,
not cryptographic authenticity; only data downloaded from a trusted endpoint
or from a manually verified exchange archive should be considered genuine.
The wallet assumes candle-based fill timing (not order-book queue/latency),
and simulated maker fills may overstate achievable profit. There are **zero
verified Kraken BTC/AUD candles and zero genuine news events** in this bundled
cache, so **no historical or forward trading profitability has been measured**.
The maker setup is a tested simulation policy, not verified real execution.

**Next: Roadmap 8 — net-P&L, costs, trade/news and health dashboard.** External
Kraken/feeds ingestion is still blocked in this execution environment and
must be validated before claiming real results.

---

# BTC/AUD Crypto Research Bot — V9 (paper-only)

**PAPER-ONLY.** No live trading adapters or exchange-order API calls exist in `paper_engine`. Do **not** put exchange API keys in this project. Latest update and blockers: [CHANGELOG.md](CHANGELOG.md).

## V9: net-of-fees hindsight and purged walk-forward (Roadmap 5)

V9 adds the research-only `hindsight` package. Completed trades are compared to a hypothetical best *future candle opening* exit in a bounded time window; alternatively, the oracle may delay entry by up to six completed 4-hour bars and choose a later opening exit. Both use **the V6 fee/spread/slippage model**. This is a hindsight upper-bound diagnostic, **not an earnable price forecast** or a live trading signal. The synthetic demo also lists *unmatched signals*, which may overlap existing positions and are **never summed as profit**.

The walk-forward validator selects among **predeclared** strategy parameters using **only the prior training period's net return**. There is an explicit purge/embargo between the training and nonoverlapping test regions. Earlier candles warm indicators but a test wallet is freshly funded and prevented from trading until the test starts. Future hindsight labels are never used to choose parameters. No trained ML is being claimed as part of V9.

```bash
# Run the entire offline suite
python3 -m unittest discover -s tests -v

# Demonstration with SYNTHETIC FABRICATED data; not real BTC/AUD
python3 -m examples.hindsight_demo
python3 -m examples.walkforward_demo

# After real BTC/AUD history is imported into the V5 SQLite candle cache:
python3 -m hindsight.cli --market-db data/market.sqlite --out reports/real_hindsight
python3 -m hindsight.cli --market-db data/market.sqlite --out reports/real_walkforward --walk-forward
```

The CLI refuses missing or gapped candles; outputs go to a **new directory** and never overwrite earlier wallets. `--interval 60` is supported and passed consistently to V8. Source labels are preserved but remain *unverified provenance* until external exchange verification is performed. A V9 research report does **not** unlock or authorise real orders.

**Honest current result:** The bundled market database contains **zero genuine Kraken BTC/AUD observations**. No real-market performance is established. The synthetic accounting test remains +0.329151% net on a fabricated sample; its best-exit hindsight difference of +5.8509 quote units is **unattainable**. The synthetic walk-forward control made **zero trades across three folds**, returning 0.0% in each. See `reports/` and `CHANGELOG.md` for details and limitations.

**Next milestone:** Roadmap 6, timestamped news and event-analysis module, after collecting verifiable market data.

## Project modules

| Module | Status |
|---|---|
| `data_layer/` | Kraken public OHLCV API/archives, SQLite storage, coverage and gap detection. Real BTC/AUD sync still not verified on this host. |
| `trading_costs/` | V6 single fee model; entry+exit maker/taker, spread, volatility/size-based slippage, optional tiers/funding/transfers. |
| `paper_engine/` | V7 SQLite simulated wallet and orders; separate from Freqtrade, never reaches the exchange. |
| `backtester/` | V8 fee-on/off backtests using exact V7 simulated ledger and net drawdown/profit/Sharpe. |
| `hindsight/` | **V9** next-open future-oracle diagnostics; purged, train-only walk-forward comparison (never future-assisted trading). |
| `research/` | Existing exploratory V3 and V4 strategies, not production-proven; no new return claim. |
| `guard/` | Original independent risk logic for legacy research/dry-run. V7 has its own persistent entry lock; not yet connected to Freqtrade. |
| `user_data/` | Legacy V3 Freqtrade strategy, dry-run only. Not identical to V7's fill model. |

## V7 paper trading — Roadmap 3

A local SQLite database records cash, pending/finalised simulated orders, market/limit/protective fills, the one open BTC/AUD position, each closed trade's **NET** quote profit, equity snapshots, and an append-only audit journal. Default starting cash A$1,000, maximum A$50 per order, maximum 5% account equity exposed, minimum A$10 order, daily account loss lock at 2%, peak drawdown lock at 5%. A lock persists through restart and **prevents new buys** but not protective exits.

**Every fill uses V6 `trading_costs.estimate_execution` and `quantity_for_quote_budget`.** Entry fee and spread/slippage are deducted from simulated cash when buying; all three apply again when selling. The stored trade ledger contains gross midpoint P&L, entry fee, exit fee, spread, slippage and **net P&L**. A database audit asserts `cash = initial_cash + realized_net_PnL - open_position_entry_outlay`; every closed trade asserts `gross - all_costs = net`.

The simulator handles a single **spot long** position. No leverage, futures, shorts, real API key access or actual order execution. Fee schedule at wallet creation is immutable; create a **new** wallet database if modifying the fee assumptions. This prevents retroactive P&L changes. Kraken published tier assumptions remain in `config/fees.json`, with uncertain spread and slippage inputs explicitly modeled.

### Start, inspect and place simulated orders

Run from project root with Python 3.11+:

```bash
python3 -m unittest discover -s tests -v

# Creates a local empty A$1,000 simulated wallet; zero live exchange connectivity.
python3 -m paper_engine.cli --db data/paper_wallet.sqlite init

# One COMPLETED four-hour bar (timestamps must be aligned Unix UTC seconds).
python3 -m paper_engine.cli --db data/paper_wallet.sqlite candle \
  --ts 1764547200 --open 100000 --high 101000 --low 99000 --close 100500 --volume 3

# Queue a hypothetical market buy up to A$50 total outlay, including entry fee.
python3 -m paper_engine.cli --db data/paper_wallet.sqlite buy --budget 50

# The order executes only on the NEXT completed candle; not at order-submission time.
python3 -m paper_engine.cli --db data/paper_wallet.sqlite status
python3 -m paper_engine.cli --db data/paper_wallet.sqlite orders
python3 -m paper_engine.cli --db data/paper_wallet.sqlite trades
python3 -m paper_engine.cli --db data/paper_wallet.sqlite verify
```

**Important:** sample OHLC prices above are placeholders, not observations or market predictions. The example timestamp must line up with the configured interval and move forward; the engine refuses gaps unless explicitly acknowledged.

For a passive simulated limit buy, use `buy --budget 50 --limit 98000`; it only fills when the subsequent candle trades strictly through the indicated price. Use `sell` to queue a manual simulated market exit or `sell --limit 105000` to queue a passive full-position exit. `cancel ORDER_ID` cancels pending orders. The `--client-id` option makes retries idempotent and rejects reused IDs with different parameters.

### Feed from the V5 data layer

Once genuine, gap-audited Kraken BTC/AUD data is available in `data/market.sqlite`:

```bash
python3 -m data_layer.cli --db data/market.sqlite export data/btc_aud_240.csv --interval 240
python3 -m paper_engine.cli --db data/paper_wallet.sqlite replay-csv data/btc_aud_240.csv --limit 1
# Submit an order using `buy`/`sell` here, then resume replay.
python3 -m paper_engine.cli --db data/paper_wallet.sqlite replay-csv data/btc_aud_240.csv
```

`replay-csv` resumes after the wallet's latest candle and skips previously processed timestamps. Consecutive missing bars cause a failure by default. Use `--allow-gap` only after manually assessing missing data; missing bars are **never fabricated**. All calls remain offline paper operations.

### Fill policy, limitations and caveats

- **Market orders:** submitted following a completed bar; hypothetical fill at the **next bar's open**. The next bar must already be available for historical replay; this is not a live fill confirmation or a real-time broker emulator.
- **Resting limit orders:** assumed filled only if a subsequent OHLC candle trades **through** the limit, with V6 maker fee/slippage assumptions. Exchange queue priority, adverse selection and partial fills are **not** simulated; maker-favorable scenarios remain uncertain.
- **Protective stop-loss and take-profit:** always checked on existing positions. If both are touched in one OHLC candle, choose the adverse stop. An open gap through the stop fills at the worse opening midpoint (plus estimated costs). A newly filled market order is protected during its first bar; an intrabar limit buy is also stopped conservatively if that bar's low crosses its stop, but is not credited a same-bar target whose sequence cannot be known.
- **Network issues:** V7 is a local event-driven accounting engine; no continuous data-feed worker, retries or dashboard are installed. Those belong to Roadmap 7/8.
- **Data integrity:** immutable fee/risk settings per wallet; single-pair and interval binding, strict UTC alignment and consecutive-bar validation, exact-repeat idempotency, durable transaction logs, SQL atomic updates, restart recovery.
- **Known modeling gaps:** slippage is estimated, not observed; orders do not model minimum lot/tick increments, actual maker queue/fill probability or liquidity depth; the daily risk lock is evaluated on candle close, not tick-by-tick. A real-time market-data feed and orderbook reconciliation would be required before treating this simulator as live-grade.

### Offline synthetic example

```bash
python3 -m examples.paper_demo
```

Writes `reports/paper_demo.json` with two labeled **synthetic** fills, stops/targets, fees and net outcome. It is a deterministic software exercise **not a measured strategy profit**.

## Test suite and research honesty

`python3 -m unittest discover -s tests -v` tests the entire preserved V3–V6 suite plus V7 paper ledger. Current test count and blockers are recorded in [RUN_SUMMARY.md](RUN_SUMMARY.md). No new genuine BTC/AUD historical returns are claimed. Do not turn on live execution; there is no live execution path in V7.

## What's next

**Roadmap 4: the unified fee-aware backtester.** It should replay real BTC/AUD historical candles through a chosen strategy and this exact paper wallet, report NET profit, net profit factor, maximum drawdown, Sharpe, fees on/off, and trade-by-trade logs. Keep any research/test data strictly out-of-sample when evaluating model selection. See [CHANGELOG.md](CHANGELOG.md).

## Roadmap 4: unified historical backtester (V8, 2026-10-24)

`backtester/engine.py` reuses the **exact V7 `PaperEngine`**, not a separate
fill simulator, with `trading_costs` fee settings on every fill. It runs a
technical Donchian-breakout baseline for measurement, not a validated AI model:

- Default **4h candle** policy: buy the 20-day (120 preceding-bar) high breakout
  if close > EMA200 and EMA50 > EMA200, sell on a break below the prior 10-day
  low or EMA200, or the conservative 10% stop managed by the paper wallet.
  Signals use only a completed bar; market orders execute at the NEXT bar's open.
- Max single position 5% of account, A$50 order cap, 12-bar cooldown; the
  V7 risk-stop, conservative same-bar stop priority and gap failure carry over.
- Compares fees **ON** to fees **OFF** using separate SQLite paper accounts,
  identical strategy rules and risk parameters. Both carry actual wallet
  gross/fee/spread/slippage/net ledgers. The return difference is a *whole
  execution-cost effect*, which can include sizing/risk-sequence differences,
  not just transaction fee dollars.
- Bar-close equity is marked at estimated *net liquidation value*, including
  exit fees and friction; open trades appear as unrealized mark-to-liquidation
  result, not as a closed profit. Reports net total return, net win rate,
  net profit factor, max drawdown, annualized Sharpe (zero risk-free, crypto
  365-day year), fees, spread, slippage, percentage of gross winning-trade
  profits consumed by trading fees, and full per-trade ledger.
- No fees if using `FeeSettings.zero()` (no spread or slippage either).
  `fees_pct_of_gross_winning_trade_profit` is `null` when no winning gross trades.
  `net_profit_factor` is `null` when no profitable/loss trades, or the string
  `Infinity` when there are winners and no losers. Sharpe is `null` for a
  constant bar-return stream.
- **Strict inputs:** validated, contiguous, UTC-aligned BTC/AUD OHLCV only;
  no imputed missing candles, duplicates or same-bar future signals. V5 data
  `source` values are preserved; this does NOT prove Kraken provenance.
  A BTC/USDT proxy must NOT be loaded under a BTC/AUD Kraken identifier.

Run on a machine with verified historical Kraken BTC/AUD data already imported:

```bash
python -m data_layer.cli report --help  # view data-layer CLI options
python -m backtester.cli --market-db data/market.sqlite --out reports/my_first_backtest
# Optionally: --interval 60 (timeframe-scaled lookbacks), --start/--end with ISO8601 offsets
```

Outputs: `metrics.json` (includes trade logs and equity curves),
`costs_on.sqlite` and `costs_off.sqlite`. Existing wallet files cannot be
silently overwritten. Both wallets are **simulation-only** and never use
Kraken trading API keys.

Offline demonstration with **fabricated bars only**:

```bash
python -m examples.backtest_demo
python -m unittest discover -s tests -q
```

**Data-access blocker:** No real Kraken BTC/AUD OHLCV has been imported into
`data/market.sqlite` in the shipped package (zero candles); this machine has
no DNS access to `api.kraken.com`. The historical net strategy return is **not
measured**. Synthetic demonstration returns only verify code behaviour, never
predict real performance. Realistic order-book slippage, queue fills, minimum
sizes and Freqtrade dry-run parity also remain unverified.

## Roadmap 5: fee-aware hindsight and walk-forward checks (V9)

Hindsight is a **research-only oracle**, never a trading signal. With the price
history already known, it enumerates a restricted menu of possible future
opening-price entries/exits after V6 modeled trading costs. It compares a
completed simulated trade's actual net profit with hypothetical alternatives,
identifies unmatched breakout signals, and marks opportunity gaps as
**not achievable / not additive to realized P&L**. It NEVER credits bar highs
as executable fills and never adds oracle opportunities to wallet profit.

Chronological evaluation uses expanding training history, an outcome-horizon
purge between train and each test, disjoint tests and strategy selection using
only training net returns. Previous test data can enter later training only
when those labels have matured. No AI model is trained by this V9 validator.

From the project root, run:

```bash
python3 -m unittest discover -s tests -q
python3 -m examples.hindsight_demo   # fabricated market; software-only test
python3 -m examples.walkforward_demo # fabricated market; software-only test

# ONLY after authentic, gap-checked Kraken BTC/AUD history is imported:
python3 -m hindsight.cli --market-db data/market.sqlite --out reports/kraken_hindsight_001
python3 -m hindsight.cli --market-db data/market.sqlite --out reports/kraken_walk_001 --walk-forward
```

A nonexistent or empty market database causes a refusal rather than creating
results. The shipped `data/market.sqlite` contains **zero BTC/AUD candles**.
The network environment cannot resolve the public Kraken API; no factual
Kraken BTC/AUD strategy P&L has been measured.

The synthetic demonstration reuses the V8 net wallet result (+0.329151%);
one simulated trade recorded +3.2915 quote units net, and a restricted future
oracle found a best next-opening exit corresponding to +9.1424 quote units net.
The +5.8509 gap and 40 unmatched signals are **hindsight only**; they are not
missed earnable profits and have no predictive content. The sample walk-forward
folds recorded zero trades and 0.0% net returns, not trading success.

**Next: Roadmap 6**, timestamped news/sentiment ingestion and retrospective
attribution using strictly point-in-time inputs. Actual market history is
still needed before evaluating a news-enhanced edge.

## V10 / Roadmap 6 — timestamped news intelligence (research-only)

`news_intelligence/` adds a **read-only** crypto news RSS collector plus a
BTC-first event-study module. There is **no link to live order placement**.

- **Sources:** CoinDesk, Cointelegraph, The Block, Decrypt and Bloomberg Crypto
  RSS, fetched over HTTPS from a host allowlist. No account credentials.
  Feed URLs are third-party endpoints; their uptime/format cannot be assumed.
- **Observability:** `published_ts` is provided by the publisher;
  `first_seen_ts` records when this bot actually received the story.
  `available_ts = max(published_ts, first_seen_ts)`. The model **cannot**
  assume it saw the story at its historical publication time if first imported
  later. Late-imported archives are not backdated as trading signals.
- **Caching:** SQLite news table, canonical URL and near-time exact-headline
  deduplication, RSS ETag / Last-Modified conditional requests, successful
  poll timestamps, per-source fetch errors and bounded retry/backoff.
- **Categorisation:** A small, auditable *rules-based* lexicon labels
  macro/regulation/ETF/security/exchange/institutional/onchain/technology
  and headline polarity (positive/negative/neutral). This is **not a
  calibrated neural sentiment model**. BTC/USD and BTC/AUD share Bitcoin
  news, but **only verified Kraken BTC/AUD candles** enter the BTC price study.
  Unrelated ETH/SOL/XRP-only articles are kept for future modules but excluded
  from BTC attribution. Bitcoin, broad-market and macro stories are eligible.
- **Studies:** baseline = last fully closed 4-hour (or selected timeframe)
  candle known when the bot first saw the story; outcome = first completed
  candle closing at or after first-seen + horizon. Reports gross percentage,
  costs-included net P&L and net return, fee/spread/slippage, and whether
  move exceeded the **V6 fee model** break-even cost + minimum edge. The
  summary groups results by category and time horizon. No within-candle
  future high/low or missing-bar imputation.
- **Research signal qualification:** candidates require >=20 older training
  observations and >=10 later holdout observations, separate positive NET
  average and positive NET outcome fraction in both, plus purging of labels
  whose horizon overlaps the holdout start. The `event_signal_asof()`
  interface refuses to use a model cutoff at/after the incoming story.
  This is **not** causal inference, control-group matched event attribution,
  or evidence of out-of-sample alpha. Candidates do NOT cause orders.

### Commands

```bash
# Pull configured public RSS feeds and record the actual time first observed.
python3 -m news_intelligence.cli --news-db data/news.sqlite sync

# Once BOTH contemporaneous news and sufficient real Kraken BTC/AUD OHLC data
# have accumulated, score fully matured news-event windows using one fee model.
python3 -m news_intelligence.cli --news-db data/news.sqlite report \
  --market-db data/market.sqlite --interval 240 --horizons 4,24,48 \
  --output reports/news_event_study.json

# Strictly fabricated sample: demonstrates timestamps, net fee outcomes,
# confidence gating, no live market access and no trades.
python3 -m examples.news_demo

# Run every regression test, including the retained 95 V9 tests.
python3 -m unittest discover -s tests -q
```

When the news or candle store is empty, `report` **fails closed**. The first
RSS fetch has not succeeded in this execution environment (DNS unavailable),
so the project ships with **zero genuine news items** and **zero verified
Kraken BTC/AUD candles**. A newly collected story must be allowed enough
forward time to mature before a 4h/24h/48h event is scored. The RSS collector
can be invoked repeatedly by a system scheduler; long-running orchestration,
news + price strategy decisions and the dashboard belong to Roadmap 7/8.

`reports/news_synthetic_demo.json` is labeled **fabricated**, not a Bitcoin
trade or a past market observation. There is no demonstrated net profit or
reliable buy/sell recommendation in V10.
