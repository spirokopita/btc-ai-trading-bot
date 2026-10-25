# V13 — Native Android paper-monitor proof of concept

**No wallet, exchange account, API key, deposit, real order, trading adapter or model-generated order is involved.** V13's Android component is a **paper-account control and public-market monitor**, not a profitable AI trading app or a port of the V12 Python decision engine. This distinction is deliberate.

## What the Android source implements

- A Compose screen with **A$1,000 simulated prefill**, **REFILL +A$1,000**, **RESET TO A$1,000**, account funding audit, and explicit simulated NET P&L excluding deposits. The current Android account holds **zero BTC**, so NET P&L is A$0 until paper trading is ported.
- An idempotent ON/OFF control. The same control is accessible through a **2×1 Glance home-screen widget**. Enabled means *periodic monitoring requested*, not uninterrupted background execution. Status shows PAUSED / WAITING / RUNNING / STALE / SUSPENDED; a sync error forces STALE.
- A **4×2 resizable dashboard widget** with paper equity, net P&L, last completed BTC/AUD 4h candle price, no-position/no-trade/AI-disabled labels, and feed health.
- A purple-accent (#7C3AED) low-priority ongoing notification while monitoring is enabled, with a Pause action. **Android/Samsung control the status-bar appearance; this app cannot make the entire system bar purple or guarantee a Live Update chip.** Permission is required on Android 13+.
- Public Kraken 4h OHLC fetch (`api.kraken.com/0/public/OHLC`), capped to the latest 12 completed candles, parsed as integer AUD cents, checked for gaps and staleness, stored locally in SQLite with duplicate timestamps ignored. **No real network request was possible from the current build environment; public fetch is implemented but not device-verified.**
- Android WorkManager unique periodic job with **15-minute minimum** and CONNECTED network constraint, plus an immediate one-time sync when enabled. No foreground service is declared. Android Doze and OEM battery rules can delay or stop periodic work. Paused state is rechecked transactionally after a network call to block late writes.
- Local SQLite account, funding audit, monitoring state, and candles. Android backup is disabled. No secrets stored.

## Build / install (requires Android SDK and Gradle)

1. Open this **`android/` directory** as a project in Android Studio. Allow Gradle to download the specified plugins/dependencies. Android SDK 35 and JDK 17 are required.
2. This archive does **not** include a Gradle wrapper JAR (the build environment had neither Gradle nor Android SDK and could not download one). Use a locally installed Gradle 8.9, or generate a wrapper with `gradle wrapper --gradle-version 8.9` before `./gradlew assembleDebug`.
3. In Android Studio, select **Build > Build APK(s)**, or run `gradle assembleDebug`. Expected output after a successful build: `app/build/outputs/apk/debug/app-debug.apk`.
4. Install the APK on an Android 8+ device, open the app, allow notifications if desired, tap START MONITOR, and add both widgets from the launcher. Verify internet/offline/restart, widget control and refill/reset before treating the build as tested.
5. For instrumented SQLite tests on a connected emulator/device: `gradle connectedAndroidTest`. These were **authored but not run** here.

**Build status:** Android Gradle compilation, APK generation, emulator/device installation, widget rendering, notifications and live Kraken calls are **UNVERIFIED**. No APK is included or claimed. The Kotlin-only core and Python static source tests were executed on the host.

## Host tests

```bash
./run_host_tests.sh
# Also from project root:
python3 -m unittest discover -s tests -q
```

## Operational safety

- The purple notification is informational, **not** a guarantee of continuous work or a foreground-service exemption.
- If disconnected, stale or suspended, no new trading entries can be made: V13 **never creates any trades**.
- WorkManager is for deferred periodic public data fetch, not low-latency intrabar trading or real-money stop execution.
- The Python V12 reference strategy/backtester has not been ported to Android; later runs should port the **paper ledger with fees** and compare it against deterministic V12 fixtures before enabling simulated orders.
- Kraken public OHLC history is limited (typically recent ~720 intervals). The 12-candle phone sample is **not** sufficient for historical AI model validation.

## V15 GitHub Actions APK build (not yet run)
Upload this entire project to a GitHub repository, then select **Actions → Android paper-only build → Run workflow**. On success, download the `btc-aud-paper-debug-apk` artifact. The job installs Android SDK tooling, Gradle 8.9, compiles `assembleDebug`, runs JVM unit tests, and fails rather than publishing an absent APK. It does **not** test on an Android device; use a real device/emulator for notifications, widgets, networking and battery behavior. No trading keys or wallet needed.
