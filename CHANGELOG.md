# Project changelog / next-run briefing

**OPEN BLOCKER (V15): Which GitHub repository should receive the Android project so GitHub Actions can actually compile and test the APK?** No repository was provided or modified in this run.

## 2026-10-25 — V15 CI build pipeline

### Current state in exactly five lines
1. V12 Python strategy/backtesting and paper engine retained; genuine BTC/AUD NET edge unverified.
2. V13 Android monitor, widgets, simulated funding and background scheduling remain source-only.
3. V14 Kotlin fee-aware single-position paper ledger retained; not integrated with UI or persistence.
4. V15 adds GitHub Actions SDK/Gradle debug APK build and JVM test workflow; remote run NOT executed.
5. Real orders: 0; real Kraken BTC/AUD NET return: NOT MEASURED; installable APK: NOT VERIFIED.

### Done
- Added `.github/workflows/android-paper-ci.yml` with least-privilege GitHub permissions, Android SDK setup, Java 17, Gradle 8.9, `assembleDebug`, `testDebugUnitTest`, artifact validation and debug APK upload.
- Added Android README instructions for manually triggering and retrieving the build.
- Local static YAML/workflow checks and retained host tests run as reported in RUN_SUMMARY.md.

### Broken / next
- This runtime cannot run Android SDK/Gradle; the workflow has not been executed on GitHub, and no APK/device result is claimed.
- **Next:** Run CI in a repository, inspect/fix actual compile errors, verify installation and widgets on device. Keep paper-only execution.

### Observed NET results
- Genuine market gross/cost/NET: NOT MEASURED. No new simulated strategy trades; no profit claimed.

---

# Project changelog / next-run briefing

**OPEN BLOCKER (V14):** Which Android SDK/Gradle-enabled build runner or GitHub Actions repository can compile and device-test the Android app? APK compilation and device verification remain unperformed.

## 2026-10-25 — Run 10 (V14 pure Kotlin fee-aware paper ledger)

### Current state in exactly five lines
1. V12 Python research and paper engine retained; historical net edge unproven.
2. V13 Android monitor, funding, notification and Glance widget sources retained.
3. V14 adds a pure Kotlin single-position paper fill/round-trip fee ledger.
4. V14 Kotlin host checks pass; Android APK/device and genuine Kraken validation remain untested.
5. Real orders: zero; real BTC/AUD NET results: NOT MEASURED.

### Done
- Added `android/app/src/main/java/com/btcaud/paper/core/PaperTradeLedger.kt` for integral-cent and satoshi paper-only accounting with fee/spread/slippage and gross/cost/NET reporting.
- Added `android/host_tests/PaperTradeLedgerHostTest.kt` for deterministic round-trip, accounting, and rejection tests.
- Compiled pure Kotlin sources with locally installed kotlinc and ran host test successfully.
- Existing app remains monitor-only; ledger is NOT wired to UI, database, trading signals or Android worker.

### Observed NET results
- Synthetic fixture only: gross +A$50.00; total modeled costs A$8.41; NET +A$41.59. This is a math fixture, NOT a real market result.
- Genuine Kraken BTC/AUD returns: NOT MEASURED. Real orders: 0.

### Broken / next
- Android SDK/Gradle missing; no APK compiled or on-device verification.
- Partial sells, exact Python V12 parity fixtures, DB persistence and strategy integration remain incomplete.
- **Next highest-value task:** Build Android APK in SDK-enabled CI, repair compile errors and execute instrumentation tests. Do not activate real orders.

---

# Project changelog / next-run briefing

**OPEN BUILD BLOCKER (Run 09 / V13):** This runtime has Kotlin JVM and Python, but **no Android SDK, Gradle or internet access for Android dependencies**. V13 Android source and 12 Kotlin host tests exist, but no APK or on-device/widget test is possible here. An Android Studio/SDK + Gradle 8.9 build runner is required. **No live wallet is required.**

## 2026-10-25 — Run 09 (V13 Android native paper monitor and refill)

### Current state in five lines
1. V12 Python trading research, fee engine, simulated wallet, news, restart-safe paper loop and read-only dashboard remain intact; 130/130 Python tests pass.
2. V13 adds `android/` native Kotlin/Compose project, local SQLite paper prefill A$1,000, auditable refill/reset and funding-adjusted NET P&L.
3. V13 implements WorkManager public Kraken 4h completed-candle polling, pause/resume, purple-accent notification and two Glance home-screen widgets.
4. Kotlin-only host tests **12/12** and Android source contract tests **5/5** pass; 5 Android instrumented tests are written but not executed.
5. **No Android APK built, no on-device test, no genuine Kraken candles imported, no AI orders, no real trades, no observed profit.**

### Done
- Native Android project: Compose control screen, SQLite paper account with prefilled A$1,000, REFILL +A$1,000, RESET, funding audit and explicit separation of deposits from profit. Default starts PAUSED.
- Local public market monitor: Kraken XBTAUD 240-minute OHLC request, integer-cent validation, reject partial/stale/gapped tails, SQLite timestamp deduplication. Offline/no network in build environment, so actual fetch remains unverified.
- Unique WorkManager periodic 15-minute job plus one-time sync on user activation; network required, safe cancellation and transactional enabled-state recheck after fetch. No foreground service or live order API.
- 2×1 one-tap ON/OFF Glance widget with idempotent fixed actions, 4×2 resizeable Glance dashboard widget with net equity/P&L, latest price, no trades, AI disabled and health state. Purple (#7C3AED) notification with Pause; system bar colour is not controllable by apps.
- Pure Kotlin model validates simulated refill/reset, overflow, stale status and completed candles; 12/12 JVM tests passed. Five Python static source/manifest contract tests passed. Five Android SQLite instrumentation tests authored, **not run**.
- V12 Python regression suite re-run: **130/130 passed**. Source-verified BTC/AUD history in bundled `data/market.sqlite`: **0 rows**.

### Broken / not verified
- No Android SDK/Gradle, so **no compiled APK**, no installation, no widget rendering test, no real notification/permission test, no Kraken network request in this environment.
- No Android paper trade/strategy engine yet; only public data monitoring and simulated funding. The V12 Python engine is a reference, not an Android runtime component.
- No evidence of a profitable trading edge; genuine market NET returns are **NOT MEASURED**. No real-money orders or wallet access.

### Next highest-value task
Build V13 with Android SDK + Gradle and run device/instrumentation tests, then fix actual compile/runtime issues before claiming an installable APK. After that, port the V12 fee-aware paper ledger with golden fixture parity tests and keep real trading disabled.

---

## Prior project changelog / next-run briefing

**OPEN BLOCKER (Run 08):** The deployment host and real Kraken BTC/AUD archive source are still unconfirmed. The current project SQLite candle cache has no genuine prices or contemporaneously collected RSS history. Which internet-connected Linux VPS will run the *paper-only* service and import source-verified history? No live trading is permitted.

## 2026-10-24 — Run 08 (V12 read-only dashboard)

### Current state in five lines
1. V5 Kraken OHLCV cache and validation are implemented; **no verified genuine BTC/AUD candles are stored** here.
2. V6 shared trading-cost engine and V7 persistent local paper wallet drive V8/V9 historical research.
3. V10 observed-time news intelligence and V11 restart-safe paper decision daemon exist but are **not deployed** and have no proven net trading edge.
4. V12 introduces a local, GET-only monitoring dashboard over the four SQLite databases with estimated NET accounting and explicit unknown-data states.
5. **130/130 unit/integration tests passed** (120 retained, 10 new), plus a clearly labeled synthetic accounting smoke example. **Real trades: zero.**

### Done
- `dashboard/snapshot.py`: opens only existing SQLite databases using `mode=ro` and connection-local `query_only`; does not create files or initiate trading. Consistent read transactions; journal/cash reconciliation errors report unavailable data instead of inventing returns.
- Portfolio accounting from V7: initial and remaining simulated cash, closed-trade gross/NET P&L, maker/taker fees on both sides, spread, slippage, win rate, last-candle estimated exit-liquidation equity, unrealized net mark-to-fee outlay and open stop/target risk. Closed-trade gross minus modeled costs is checked against NET.
- V5 market candle coverage (latest source label and recent 2,000-bar gap scan per timeframe), V10 observed-time news/feed attempts and V11 read-only decision/heartbeat journal integration. Synthetic provenance and stale observations flagged.
- `dashboard/server.py`: Python standard-library `ThreadingHTTPServer`, static local assets + `GET /api/status`; rejects POST/PUT/PATCH/DELETE, non-loopback binds, hostile Host headers and unknown paths; no third-party assets or real-exchange API calls. Security headers, `no-store`, Content-Security-Policy.
- `dashboard/static/`: responsive black-and-white presentation, 15-second auto-refresh, net equity SVG, fee breakdown, trade/market tables, simulated orders, headlines/decision evidence and diagnostic warnings. No clickable trade actions. Does not execute JavaScript from untrusted article names.
- Added 10 tests: DB absence/invalid file, cash/net/trade cost reconciliation, open-position liquidation parity, stale/lock warnings, source/time metadata, read-only file integrity, accounting corruption refusal, GET-only/Host header HTTP safety and remote-bind refusal. New demo runs on fabricated numbers in a temporary DB and is labeled SYNTHETIC.

### Results (NET of fees)
- **Actual historical BTC/AUD net performance: NOT MEASURED**. Genuine Kraken cache still has 0 candles; no live orders or real balances exist.
- Synthetic dashboard reconciliation-only demonstration: one closed simulated trade, gross +2.478619 quote units, fees 0.812975, spread 0.040649, slippage 0.022498, **NET +1.602497**. Not genuine price action, a prediction, or evidence of profitability.
- **130 tests passed** (120 retained V11 + 10 new dashboard tests). HTTP access returns JSON but does not allow any mutation.

### Broken / incomplete / risks
- No verified exchange archive/history, contemporaneous news history, or deployment machine. The dashboard can only display present local DBs; empty caches truthfully show UNKNOWN/NO DATA.
- Estimates use the same V6 cost model and last processed candle; not current bid/ask, actual fill depth or live profit. Maker-order probability, latency and partial fills are not established.
- Dashboard is localhost-only and unauthenticated; for use from a phone another device needs authenticated forwarding. Never expose the dashboard directly to the internet.
- Gap count on the dashboard covers latest 2,000 records per timeframe; full data history requires V5 audit.
- Strategy alpha is unproven; displaying attractive graphs must not be interpreted as proof of net profitability.

### Next single high-value task
**Deployment & real-data validation gate:** on an authorised network-connected Linux machine, ingest and verify authentic Kraken BTC/AUD historical bars and current public RSS feeds, validate candle gaps and fees, deploy the paper-only loop/dashboard under limited privileges, and then conduct an untouched forward paper run. Don't enable actual orders or assume any profits.

---

## 2026-10-24 — Run 07 (V11 resilient PAPER strategy daemon)

### Current state in five lines
1. V5 Kraken multi-interval SQLite OHLCV cache exists, but authentic Kraken BTC/AUD history has **not** been imported here.
2. V6 fees, spread and slippage drive V7 paper wallet and all V8/V9 fee-aware research components.
3. V9 hindsight/train-test analysis and V10 first-observed RSS event study remain research-only, not demonstrated profitable.
4. V11 adds fail-closed 24/7 PAPER-only strategy loop integrating Donchian trend breakouts with strictly earlier qualified news and minimum NET edge.
5. **120/120 regression tests pass**, zero real trades or historical trading P&L measured; Roadmap 8 dashboard is next.

### Done
- `strategy_loop/engine.py`: fresh completed Kraken BTC/AUD candles only, strict source/time/gap checks, complete warm-up with no retrospective entries, deterministic one-decision-per-bar journal, restart persistence via V7 SQLite wallet, EMA/Donchian buy/sell and protective exit handling.
- Entry gate: strictly recent actually-observed BTC/MARKET/MACRO-positive article; event evidence uses only *earlier* matured labels and purged chronological holdout. Requires >=20 training and >=10 validation events and positive NET outcome fractions/means; conservative train/holdout mean gross move then checked through the V6 fee-aware expected-net rule (at least +0.5% NET, not just positive gross). Without evidence, HOLD.
- Default passive maker-limit entry 10bps below last close and cancel if unfilled after 3 bars. The V7 paper engine's conservative strict-through OHLC fill behavior and protective stop-loss/take-profit stay in force. Fees include both sides plus spread and slippage; no unverified maker-fill assumption is credited as earned profit.
- `strategy_loop/cli.py`: `once`, unattended `serve` (public no-key Kraken/news sync, bounded polling/backoff, independent feed error handling), `status`, single-process Linux `fcntl` lock and heartbeat/error journal. Failed feeds block new buys but do not disable existing protective simulated sells.
- `deploy/crypto-paper-bot.service.example`: **uninstalled** secure service template requiring user-supplied non-root Linux setup, no trading credentials.
- `tests/test_strategy_loop.py`: 13 new tests for replay idempotency, news-availability timing, maker expiry/trade-through, full round-trip cost gate, stale/gapped/untrusted price refusal, simulated stop under feed outages, and Linux singleton lock.
- `examples/strategy_loop_demo.py`: fabricated 700-bar restart demo processed once, 2nd iteration processed zero bars, wallet validated. **No orders and no P&L**; only architecture test.

### Results (NET of fees)
- **Actual historical/live BTC/AUD P&L: NOT MEASURED**. No real OHLC feed, source-qualified events, profitable AI model or execution established.
- **Fabricated local test:** starting 1,000 simulated quote units; ending 1,000 units, **net 0**, no completed trades and no claimed earnings. Mocked-news unit tests exercise order plumbing only; they are NOT market results.
- Full regression suite **120 tests passed** including 107 retained V10 tests. CLI correctly refused to run with the empty market cache.
- **Live exchange orders placed: 0.** No live execution code was enabled or added.

### Broken / incomplete / risks
- No verified Kraken BTC/AUD candle backfill or live RSS first-observation data. Without sufficiently matured news-event evidence, V11 intentionally cannot open positions.
- Market provenance stored in SQLite is a source label, not independent verification; users must obtain actual data from the exchange. News correlations can be spurious; strict filters are not proof of predictive alpha or calibrated model estimates.
- Candle-only limit fill model cannot model queue position, partial orders, impact or real maker fill likelihood. Modeled slippage/spread also need comparison to genuine trade/order-book data.
- Networked host deployment, restart-on-boot and monitoring have not been performed here. Cron/systemd example provided only.
- Restarting after missing candles fails closed; open **paper** positions cannot be updated without a valid sequential candle feed. Any eventual live-grade counterpart needs tick-level protections and broker reconciliation.

### Next single roadmap item
**8. Read-only dashboard** for whole-account gross and net P&L, actual simulated entry/exit fee components, open risk, recent orders, validated news evidence and feed/loop health. Must display missing data and empty-account states truthfully and must not trigger orders.

## 2026-10-24 — Run 06 (V10 news intelligence, no trade execution)

### Current state in five lines
1. V5 Kraken multi-timeframe historical storage exists; **zero authentic Kraken BTC/AUD candles** are verified in this environment.
2. V6 provides the single configurable fee, spread and size/volatility slippage cost engine used in all offline examples.
3. V7 persistent paper wallet and V8 net-fee backtester are unchanged; risk locks and the absolute prohibition on live trading remain in place.
4. V9 adds fee-adjusted hindsight oracles and purged walk-forward validation; no profitable BTC/AUD edge has been established.
5. V10 adds observed-time-aware BTC-first RSS ingestion and fee-aware news/price event studies; **107/107 tests pass**, market/news empirical effectiveness unmeasured.

### Done
- New `news_intelligence/feeds.py`: bounded, HTTPS-allowlisted RSS/Atom collector for five public outlets with ETag/Last-Modified support, retries of transient errors, XML DOCTYPE/ENTITY rejection, timezone-aware publication dates, and per-feed failure isolation.
- New `news_intelligence/store.py`: persistent SQLite cache with unique canonical URL, title syndication deduplication, actual bot first-seen timestamps, category/asset tags and ingest state. Late historical article publication is **not** misrepresented as a tradable contemporaneous observation.
- New `news_intelligence/signals.py`: transparent rule-based sentiment/event tags, BTC vs altcoin scope, event return windows from LAST KNOWN completed candle to FIRST qualifying future closed candle. V6 fees, spread and slippage determine **net** outcomes and break-even threshold. Categories summarise material movement frequencies; associations explicitly do **not** demonstrate causation.
- The as-of study CLI strictly ignores not-yet-completed future candles and refuses to report from an empty, invalidly-sourced or gapped BTC/AUD price series.
- `train_signal_quality` uses chronological category-level training/holdout with purged label windows; `event_signal_asof` allows only research candidate annotations based on strictly earlier matured evidence. **No autonomous trading signal is installed into V7**; that is Roadmap 7.
- Added `news_intelligence/cli.py`, an explicitly SYNTHETIC demo and 12 new unit tests. Full regression suite **107 tests passed** with 95 retained tests; no real orders.

### Results (NET of fees)
- **Genuine news-conditional BTC/AUD net returns: NOT MEASURED.** First direct CoinDesk RSS access failed `URLError: Temporary failure in name resolution`. Existing Kraken candle cache still has zero verified genuine observations.
- **SYNTHETIC accounting example only:** a fabricated Bitcoin ETF headline accompanied by a 0.0993% future upward midpoint move yielded a **-1.6119% simulated entry-to-exit return after estimated fees/spread/slippage**. The example produces **zero qualified news signal categories** due to tiny sample size. The price and story are fabricated; this is a program validation, not an earned or historically missed trade.
- 107/107 local `unittest` tests passed. No investment recommendations or live trades were generated.

### Broken / incomplete / risks
- DNS/network access to public news and Kraken markets is unavailable here. No 24/7 collection daemon or real article archive was established, so don't claim that macro/ETF/news predicts BTC.
- Rules-based lexicon sentiment can misunderstand irony, negatives, entities and topic salience. Publisher timestamps, editorial publication delays and overlapping articles are imperfect; first-seen protects simulated signal timing but doesn't prove universal availability.
- Price moves around articles are **correlations**, not causal event impacts. No matched controls or adequate independent holdout sample exists. ATR- and orderbook-calibrated live slippage is still unverified.
- The event-study is descriptive and not integrated with execution; its research candidate does not authorise trades.

### Next single roadmap item
**7. Combine causal/available historical price indicators with only validated news candidate signals into a continuously running, restart-safe **PAPER-only** decision loop. Fail closed until real candles/news are ingested and fee-aware thresholds are met.**

## 2026-10-24 — Run 05 (V9 fee-adjusted hindsight + purged walk-forward)

### Current state in five lines
1. V5 multi-timeframe Kraken BTC/AUD cache and import logic exist, but zero verified real candles are stored here.
2. V6 fee/spread/slippage engine is shared across V7 wallet and V8 backtester and new V9 diagnostics.
3. V7 provides persistent SQLite-only simulated trades, risk locks and a reconciled ledger; no broker order calls.
4. V8 computes fee-on/off net returns, trade metrics, drawdown and Sharpe; strategy edge remains unproven.
5. V9 adds counterfactual net-fee oracle analysis and train-only purged walk-forward validation; automated tests pass and live trading stays disabled.

### Done
- New `hindsight/analysis.py`: scores completed V8 trades against the best possible **future open-to-open** exit within a 60-bar window, and separately the best hypothetical delayed entry/exit within six delayed openings. Uses **V6 unified fees, spread and size/volatility slippage**, and explicit matching of entry/exit timestamps to the candle series.
- Reports realized **NET P&L** alongside oracle net/gross/fees/spread/slippage, possible early/late exits, and differences. An oracle selects future opening prices with knowledge of the future; it **cannot be traded** and must never be combined with earned profit.
- Identifies unexecuted strategy buy signals, calculates their hindsight net opportunity after costs, and warns that overlaps, pending orders, opportunity capital and risk locks make them non-additive, non-executable what-ifs.
- New `hindsight/walkforward.py`: a predeclared, small parameter grid is selected on **training-only net backtest return**, with purged chronological, nonoverlapping tests. Each test uses a clean V7 wallet; prior bars are used for indicator warm-up without allowing trades. The future oracle is diagnostics only, never an input for parameter selection.
- `hindsight/cli.py`: offline real-market-store report, `--walk-forward` option, configurable bar horizons and timeframe, strict empty/gapped-candle rejection. Fixed a discovered CLI bug so the non-default `--interval` is also passed into the ordinary V8 backtest.
- Added synthetic-only hindsight and walk-forward examples plus unit/integration tests for identical ledger accounting, net fees, oracle limits, missing-data refusal, non-default timeframe and mutation-of-heldout-prices leakage regression.

### Results (NET of fees)
- **Genuine Kraken BTC/AUD returns: NOT MEASURED** — local candle cache contains zero observations. No real orders placed.
- **SYNTHETIC software example**, 700 fabricated 4h bars: one realized paper trade and **+0.329151% account return after costs** (same V8 smoke test), versus hypothetical best later-opening exit **+9.1424 quote units** on the trade and actual realized trade **+3.2915 quote units**. The **+5.8509 quote-unit difference is unattainable oracle hindsight**, NOT profit or a performance forecast. No result was tuned using actual market data.
- Synthetic example: 40 unmatched prior-close entry signals scored and 40 positive-oracle opportunities; these **must not** be summed as earnings. Separate synthetic walk-forward example scored 3 future folds; each **0.0% net**, **zero trades**. This merely checks temporal separation, not model quality.

### Broken / risks
- Genuine Kraken BTC/AUD archives/network fetch, actual spread/depth, exchange-minimum orders, real slippage and partial fills remain unverified.
- Oracle scans future opening prices and can ignore protective stops, available cash, overlapping positions and fill probability; it is a **research upper bound, not an achievable trade plan**.
- No trained ML was added in this task. The small train-only grid is a test of strategy-parameter separation, **not proof of out-of-sample predictive advantage**. Years already examined elsewhere may be contaminated by earlier researcher decisions.
- Current walk-forward test periods may have no actual trades; do not interpret 0.0% synthetic returns as evidence the strategy is safe or profitable.

### Next single roadmap item
**6. Timestamped crypto/macro news and sentiment module** with sources, event-before/after attribution and a strict publish-time firewall. Genuine market data provenance and first networked Kraken backfill remain prerequisites for credible live-like event studies.

## 2026-10-24 — Run 04 (V8 unified fee-aware backtester)

### Current state in five lines
1. V5 Kraken BTC/AUD historical-data cache remains empty; genuine market test data have not been ingested here.
2. V6 trading-cost model is still the single source of fees, spread, and size/volatility slippage.
3. V7 SQLite paper wallet is now reused unmodified for V8 historical replay and its reconciled fills/realized P&L.
4. V8 implemented paired cost-on/cost-off replays with net performance, win rate, net profit factor, drawdown, Sharpe and full ledgers.
5. **78/78 tests passed**, no real-data profits measured and real-money execution remains unavailable/disabled.

### Done
- `backtester/engine.py`: strict OHLC validation, causal Donchian 20-day breakout and 10-day low/EMA200 exits, prior-EMA trend filter, next-open order fills, previous-bar ATR-based cost inputs, 10% protective stop and enforced cooldown.
- Historical runs dispatch buys, sells, targets and stops exclusively via V7 `PaperEngine`, preserving its persistence, spread/slippage/fee charges and risk halts.
- Separate `costs_on.sqlite` and `costs_off.sqlite` outputs, immutable fresh wallets, full trade logs plus bar-close net liquidation equity series. Side-by-side returns include full fees-on/off comparison and audit.
- Metrics: net account P&L, gross and net completed trade totals, net win rate, net profit factor, fee/share-of-gross-positive-pnl, spread/slippage, max drawdown and annualized Sharpe; zero-divisor metrics are explicitly null rather than made up.
- CLI on V5 Kraken BTC/AUD storage, strict no-imputation gaps, honest provenance metadata. Synthetic demonstration isolated in `examples/backtest_demo.py`.
- 12 new backtester tests + 66 retained tests = **78 passing** without resource leaks.

### Results (NET of fees)
- Genuine BTC/AUD performance: **NOT MEASURED**; shipped candle cache contains zero rows.
- SYNTHETIC price-path smoke test: 700 generated 4h candles, one round-trip trade; fees ON net account return **+0.32915%** (end 1003.2915 from 1000) vs all execution friction OFF **+0.42509%**. Trading fees **0.8266**, spread **0.0413**, slippage **0.0540** quote units. NOT historical or predictive.
- Real orders placed: **0**.

### Broken / risks
- No real Kraken BTC/AUD archive or public API response on this host (DNS inaccessible); cannot claim strategy works on market data.
- Intrabar path, passive limit fill probability, order-book impact, exchange lot/tick minima and exact Freqtrade dry-run parity are not modeled or verified.
- The fee-off comparison removes *all* modeled friction; return differences may also reflect sizing/risk paths. Do not interpret as simply fees paid.
- Strategy is a fixed baseline without trained ML; historical proxy backtests elsewhere do not prove forward net returns.

### Next single roadmap item
**5. Hindsight net-of-fees trade opportunity analysis** with predeclared benchmark and lookahead-safe train/test and walk-forward validation. Obtain authentic market data first to make profit/loss measurements meaningful.

## 2026-10-24 — Run 03 (persistent paper wallet)

### Current state in five lines
1. V5 public Kraken BTC/AUD historical data layer exists; networked ingestion and multi-year historical coverage remain unverified.
2. V6 costs module remains the **single source of execution and fee estimates**; default retail Kraken spot tier is modeled, not confirmed from real fills.
3. **V7** adds a persistent, locally simulated BTC/AUD spot wallet, market/limit orders, fills, stop/target exits, a full NET-P&L ledger and restart recovery.
4. V3/V4 trading strategy profitability remains unproven. Real Kraken BTC/AUD trading results remain **unmeasured**; all new sample candles are synthetic.
5. Paper-only safety remains absolute: no exchange-order functionality is connected; the V7 engine processes only provided offline candle data.

### Done
- `paper_engine/engine.py`: atomic SQLite ledger for cash, equity snapshots, simulated open position, unique/client-idempotent market and limit orders, maker/taker fills, stop/target protective exits, audit journal and cancellation.
- All new trade executions and position budgets use `trading_costs` for entry and exit costs. Net P&L is calculated from **actual simulated cash flows** and separately reconciles to gross less maker/taker fees, spread and slippage.
- Persistent risk settings: default A$1,000 starting cash, A$50 maximum order, 5% maximum exposure, 2% daily loss lock, 5% high-water drawdown lock. The lock rejects new buys after a breach, survives restart, and permits existing position exits.
- Candle processor guards against time travel, duplicate processing and unacknowledged history gaps; stop beats target in ambiguous OHLC bars; gaps through stops exit at opening quote, not at an unachievable stop.
- Newly filled market orders activate stops in the opening bar; for limit fills with unknown intrabar ordering, the stop is assumed if crossed, and same-bar targets are not credited.
- `paper_engine/cli.py` supports initialization, place/cancel offline orders, candle playback, replay CSV, status, trades, orders and reconciliation checks.
- `examples/paper_demo.py` generates an explicitly synthetic two-trade accounting report; `tests/test_paper_engine.py` verifies cash/fees, fills, restart, risk, gaps, rollback, maker/taker and idempotency.

### Results (NET of fees)
- New real-market BTC/AUD test trades or profit: **none**. Zero real orders.
- Offline synthetic example on arbitrary candles: initial 1,000 quote units, ending **998.3694**, combined **NET −1.6306**, total entry+exit fees 1.5870, modeled spread 0.0793 and slippage 0.0439. Not a performance forecast or historical replay.
- **66/66 automated tests passed**. No genuine Kraken connectivity was required or tested.

### Broken / incomplete / risks
- The standalone paper engine is not an always-on collector; a worker reading completed price bars, outage recovery and remote monitoring remain pending later roadmap steps.
- Native Freqtrade dry-run is not reconciled with this wallet. No live-grade execution fidelity is claimed: partial fills, book queue positioning, minimum lots/ticks and real spread/impact are absent.
- The OHLC replay assumes next-bar opening fills after an order placed on a prior bar and pessimistic stops on ambiguous candles. Real-time paper trading needs a feed that can actually observe those executions.
- No proven profitable strategy exists yet; original V3/V4 reports remain research artifacts, not real investment returns.
- Multi-year Kraken BTC/AUD history and a real API ingestion run on a networked host are still pending.

### Next single roadmap item
**4. Fee-aware, unified backtester** using genuine Kraken BTC/AUD from V5 when available, the exact V7 wallet, independent fee-on/fee-off controls, net profit factor, Sharpe, drawdown, net win rate, and gross/fee/net trade breakdown. Do not optimise on test-set data.

## 2026-10-24 — Run 02 (unified fee model)

### Current state in five lines
1. V5 Kraken multi-timeframe candle cache persists; real Kraken API sync remains unverified on this host.
2. V3 trade-outcome labels and V4 breakout proxy research are unproven; past strategies lost money on BTC/USDT proxy tests.
3. V6 now has one configurable `trading_costs` engine shared by research labels, fills, and candidate-trade estimates.
4. Risk controls and dry-run-only setup remain; V3 Freqtrade entry now explicitly rejects `dry_run=false` rather than relying on an arming file.
5. **44/44 local tests pass**, and both legacy research engines passed a synthetic-data smoke replay; **zero genuine market results** were measured today.

### Done
- `trading_costs/model.py`: maker/taker execution fees on both sides, optional USD-denominated volume tiers, spread and volatility/order-size slippage, funding for simulated perpetuals, opt-in transfer/network charges, budget-aware sizing, expected-net decision gate, minimum break-even gain and fully reconciled per-trade ledger.
- `config/fees.json`: exchange-configurable retail Kraken spot fee assumptions 0.40% maker/0.80% taker at initial tier, with partial 30-day USD volume tiers; spread/slippage figures are adjustable **assumptions**.
- `trading_costs/cli.py`: offline fee-inclusive net P&L and break-even calculator.
- Changed V3 and V4 future-outcome labels and research executions to call the new module, replacing competing hardcoded percentage formulae. V4 CLI produces a no-fee reference for technical rules.
- Every completed V3/V4 research trade now carries a gross P&L, both fee line items, modeled spread, slippage, funding, total costs and **NET P&L** in its log.
- `docker-compose.yml` mounts read-only cost package/config for Freqtrade strategy target calculations; `BtcAudEdgeV3` rejects real execution if dry-run is false even if an old arming marker exists.
- 16 new/expanded integration/cost checks and 28 retained tests all passed (44 tests total). V3 and V4 research scripts also smoke-ran on labeled **synthetic candles**, not market evidence.

### Fee example (not an actual trade)
- Midpoint buy A$100,000/BTC, midpoint sell A$104,000/BTC, total budget A$50, assumed ATR ratio 2%, market/taker fills.
- Gross profit A$1.9813; trading fees A$0.8084 (entry A$0.3968, exit A$0.4115); modeled spread A$0.0404; modeled slippage A$0.1032; **net A$1.0293**, or +2.06% on A$50.
- Estimated break-even price move ~1.90%; numbers depend strongly on *assumed*, not observed, spread/slippage and tier.

### Results (NET of fees)
- **No new real-market or validated backtest returns**. Implementation and synthetic integration tests only, not a profit claim.
- Synthetic V4 smoke check (2022-10-01 to 2023-05-31, generated candles): technical replay with modeled fees -1.237%, same replay with all costs disabled -0.715%; six closed trades each. **DO NOT interpret as BTC history.**
- Synthetic V3 smoke check: one trade, modeled net account equity 996.89 from 1000 (generated candles only).
- No money placed at risk; **0 real trades**.

### Broken / incomplete / risks
- Freqtrade's built-in dry-run execution/accounting uses its own broker fill and fee handling. Actual native runtime P&L is **not yet reconciled** to `trading_costs` because the modular wallet doesn't exist. No claim that all platforms share identical fills.
- Kraken order-book spread/depth and actual slippage have not been sampled; input values are configuration estimates. Funding is a linear signed-rate approximation, not an exchange-specific funding settlement feed.
- Tier schedules can change; only the first five current example USD-volume tiers are listed, and other exchanges need their own profile.
- Multi-year Kraken BTC/AUD archive remains missing. Native strategy/Freqtrade/Docker end-to-end was not run (dependencies/exchange access unavailable).
- Synthetic data is **not valid for estimating strategy profitability**. Existing research may be overfit; preserve unseen data.
- No multi-order asynchronous paper wallet exists yet. Ensure fee ledger, risk lock and account balances reconcile exactly in Roadmap 3.

### Next single roadmap item
**3. Paper-only trading engine** with wallet, order lifecycle, position sizing, stop/target, full fee ledger, restart persistence and audit checks. Integrate strictly with `trading_costs`, with orders never reaching Kraken.

## 2026-10-24 — Run 01 (data layer)

### Current state in five lines
1. V3 paper-only FreqAI trade-outcome model exists but has no established trading edge.
2. V4 breakout research exists and showed a preliminary proxy backtest profit; it was not validated on genuine Kraken BTC/AUD.
3. Independent risk guard and dry-run Freqtrade configuration remain available; no exchange credentials are bundled.
4. **V5** added a Kraken BTC/AUD multi-timeframe historical-data layer with SQLite storage, backfill imports and explicit gap reports.
5. **28 automated tests PASS** for all retained components (11 data tests + 17 retained tests); no networked exchange integration test completed.

### Done
- `data_layer/storage.py`: schema, per-pair/per-interval candle primary keys, candle integrity checks, bulk upsert, source provenance, ingestion-event log, UTC CSV export, coverage summaries and nonfabricated gap reports.
- `data_layer/kraken.py`: free public Kraken OHLC requests for intervals `1,5,15,30,60,240,720,1440` min; bounded 429/5xx and transient API retries, `Retry-After`, request pacing, candle finalization, incremental update checkpoint, 720-bar history warnings.
- `data_layer/cli.py`: `sync`, `import-csv`, `import-zip`, `report`, `export`.
- Chunked official Kraken OHLCVT ZIP/CSV import (10k candles at a time); doesn't mix BTC/USD or BTC/USDT into BTC/AUD.
- Kept V4 breakout research alongside V3 dry-run framework. No live trade execution added or enabled.
- Offline tests passed: timestamp alignment, wrong OHLC rollback, duplicate/idempotent ingestion, zip pair matching, rate-limit recovery, closed-candle filtering, incomplete archive warnings, cross-pair safety, UTC export and retained V3/V4 regression tests.

### Results (net of fees)
- **No newly measured net trading return**: this run implemented infrastructure, not a new trading strategy/backtest. Historical research remains preliminary and is not presented as live performance.
- **Real Kraken BTC/AUD candles ingested in this environment: 0.** No genuine archive bundled; do not treat mock/API fixtures as real prices.
- **Live orders placed: 0.**

### Broken / incomplete / risks
- Outbound DNS/network access from this execution environment failed when requesting Kraken and Coinbase public APIs; therefore no end-to-end REST response verification or actual BTC/AUD historical download occurred.
- Multi-year genuine Kraken history needs the official full archive or the Kraken Trades endpoint, followed by recent API updates. The official archive is several gigabytes; V5 does not download all parts automatically.
- Strict 4-hour V4 backtester can reject Kraken no-trade gaps; gap policy should be explicit rather than quietly fabricating candles.
- No overlapping-job lock, monitoring or retryable daily scheduler is installed; `cron` is documented as an example only.
- 2025–2026 analysis has already been studied repeatedly, so future model tuning on these years risks overfitting. Preserve new truly out-of-sample periods.
- Live execution must remain DISABLED. Running existing Freqtrade config is paper-only; full end-to-end Freqtrade integration remains unverified.

### Next single roadmap item
**2. Configurable fee model** shared by paper wallet, signals, backtester and trade ledger. Separate maker/taker, per-side charges, volatility/order-size slippage, spread, optional perpetual funding and volume tiers; report gross and **NET** P&L for every trade. Test against fee-off baseline. Do not modify strategy parameters until this is done.

## Roadmap state
1. Data layer — **implemented & offline-tested**; pending first real Kraken sync and archive import on networked host.
2. Fee model — **implemented & locally tested**, external Freqtrade dry-run reconciliation pending.
3. Paper engine — **implemented and locally tested**, pending genuine market feed and Freqtrade reconciliation.
4. Backtester — **implemented, locally tested**; authentic BTC/AUD dataset still pending.
5. Hindsight/missed-moves — **implemented & tested on synthetic data**; historical validation blocked.
6. News module — **NEXT**.
7. Combined strategy loop — pending.
8. Dashboard — pending.
