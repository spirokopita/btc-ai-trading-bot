import com.btcaud.paper.core.*
fun main() {
 val buy = PaperFill(PaperFill.Side.BUY, 1_000_000L, 10_000_000L, 26, 10, 5)
 val sell = PaperFill(PaperFill.Side.SELL, 1_000_000L, 10_500_000L, 26, 10, 5)
 val t = ClosedPaperTrade(buy, sell)
 check(buy.grossCents == 100_000L && sell.grossCents == 105_000L)
 check(t.grossPnlCents == 5_000L && t.totalCostsCents == 841L && t.netPnlCents == 4_159L)
 val start = PaperLedger(200_000L)
 val afterBuy = start.buy(buy)
 check(afterBuy.cashCents == 99_590L)
 val afterSell = afterBuy.sell(sell)
 check(afterSell.cashCents - start.cashCents == t.netPnlCents)
 check(afterSell.btcSats == 0L)
 check(runCatching { start.sell(sell) }.isFailure)
 check(runCatching { PaperLedger(1L).buy(buy) }.isFailure)
 check(runCatching { ClosedPaperTrade(sell, buy) }.isFailure)
 check(runCatching { PaperFill(PaperFill.Side.BUY,1,1,-1,0,0) }.isFailure)
 println("PASS: 9 paper-ledger checks; synthetic gross=5000 costs=841 NET=4159 cents")
}
