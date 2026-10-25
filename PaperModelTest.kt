package com.btcaud.paper.core

private fun expect(condition: Boolean, message: String) { if (!condition) error(message) }
private inline fun <reified T: Throwable> expectThrows(block: () -> Unit) {
    try { block() } catch (e: Throwable) { if (e is T) return else throw e }
    error("Expected ${T::class.simpleName}")
}

fun main() {
    var tests = 0
    fun check(name: String, block: () -> Unit) { block(); tests++; println("PASS $name") }
    check("prefill is A$1000, no wallet or trades") {
        val a = PaperAccount(); expect(a.cashCents == 100_000L, "wrong prefill")
        expect(a.cumulativeFundingCents == 100_000L && a.netPnlCents == 0L, "false profit")
    }
    check("refill adds funds without claiming P&L") {
        val a = PaperAccount().refill().refill(50_000)
        expect(a.cashCents == 250_000L && a.cumulativeFundingCents == 250_000L, "refill")
        expect(a.netPnlCents == 0L && a.refillCount == 2, "deposit falsely counted as profit")
    }
    check("reset returns to default prefill") {
        val a = PaperAccount().refill().reset()
        expect(a.cashCents == 100_000L && a.refillCount == 0 && a.resetCount == 1, "reset")
    }
    check("refill rejects zero and negative and huge deposits") {
        expectThrows<IllegalArgumentException> { PaperAccount().refill(0) }
        expectThrows<IllegalArgumentException> { PaperAccount().refill(-1) }
        expectThrows<IllegalArgumentException> { PaperAccount().refill(100_000_001) }
    }
    check("refill detects overflow") {
        expectThrows<ArithmeticException> { PaperAccount(Long.MAX_VALUE, 1).refill() }
    }
    check("OFF always shows paused") {
        expect(MonitorPolicy.status(false, null, 10L) == MonitoringStatus.PAUSED, "off")
        expect(MonitorPolicy.status(false, 1L, 100_000_000L) == MonitoringStatus.PAUSED, "off stale")
    }
    check("ON before first fetch is waiting") {
        expect(MonitorPolicy.status(true, null, 100L) == MonitoringStatus.WAITING, "waiting")
    }
    check("recent success is running") {
        expect(MonitorPolicy.status(true, 1_000L, 1_000L + 10_000L) == MonitoringStatus.RUNNING, "fresh")
    }
    check("late success is stale and then suspended") {
        expect(MonitorPolicy.status(true, 1_000L, 1_000L + 50L * 60_000L) == MonitoringStatus.STALE, "stale")
        expect(MonitorPolicy.status(true, 1_000L, 1_000L + 3L * 60L * 60_000L) == MonitoringStatus.SUSPENDED, "suspended")
    }
    check("future timestamps cannot be healthy") {
        expect(MonitorPolicy.status(true, 2_000L, 1_000L) == MonitoringStatus.STALE, "future")
    }
    check("unfinished candle is rejected") {
        val start = 1_800_000_000L // divisible by 14400
        expect(start % MonitorPolicy.CANDLE_INTERVAL_SECONDS == 0L, "test setup")
        expect(!MonitorPolicy.isCompletedCandle(start, start + 14_399), "partial candle")
        expect(MonitorPolicy.isCompletedCandle(start, start + 14_400), "complete candle")
        expect(!MonitorPolicy.isCompletedCandle(start + 1, start + 20_000), "unaligned candle")
    }
    check("error state overrides recent success") {
        val state = MonitorSnapshot(true, 1000L, 1000L, null, null, "network failure", PaperAccount())
        expect(state.status(2000L) == MonitoringStatus.STALE, "failed feed shown as healthy")
    }
    println("$tests/$tests pure Kotlin tests passed")
}
