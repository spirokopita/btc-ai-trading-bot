"""Historical, offline BTC/AUD PAPER replay; never calls an exchange API."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from .engine import (BacktestParameters, candles_from_store, compare_costs)


def _utc(value):
    if value is None:return None
    date=datetime.fromisoformat(value.replace('Z','+00:00'))
    if date.tzinfo is None:raise ValueError('Use timezone-aware dates, e.g. 2026-01-01T00:00:00+00:00')
    return int(date.astimezone(timezone.utc).timestamp())


def main(argv=None):
    ap=argparse.ArgumentParser(description='OFFLINE BTC/AUD OHLC backtest: V7 wallet, fees ON vs OFF')
    ap.add_argument('--market-db',default='data/market.sqlite',help='Existing V5 Kraken candle store')
    ap.add_argument('--out',required=True,help='NEW results directory (no wallet overwrite)')
    ap.add_argument('--interval',type=int,default=240,choices=[1,5,15,30,60,240,720,1440])
    ap.add_argument('--start',help='Optional inclusive ISO8601 UTC start, requires offset')
    ap.add_argument('--end',help='Optional inclusive ISO8601 UTC end, requires offset')
    args=ap.parse_args(argv)
    # Constructing CandleStore creates an empty database; avoid claiming successful
    # collection when the market path was missing.
    if not Path(args.market_db).is_file():
        ap.error('Market database not found: import Kraken BTC/AUD historical candles first')
    try:
        start,end=_utc(args.start),_utc(args.end)
        if start is not None and end is not None and start>end:
            raise ValueError('start is later than end')
        candles,provenance=candles_from_store(args.market_db,args.interval,start,end)
        result=compare_costs(candles,args.out,params=BacktestParameters.for_interval(args.interval))
    except (ValueError,FileExistsError) as error:
        ap.error(str(error))
    result['provenance']=provenance
    output=Path(args.out)/'metrics.json'
    output.write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps({'mode':'PAPER_ONLY','source':provenance,
      'fee_on_net_return_pct':result['fee_on']['total_return_net_pct'],
      'fee_off_return_pct':result['fee_off']['total_return_net_pct'],
      'trades_fee_on':result['fee_on']['completed_trades'],
      'output':str(output)},indent=2))


if __name__=='__main__': main()
