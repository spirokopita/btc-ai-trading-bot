"""Generate a DRY-RUN-ONLY configuration. It never enables live trading."""
import json
import secrets
from pathlib import Path

root = Path(__file__).resolve().parent
u = root / 'user_data'
(u / 'strategies').mkdir(parents=True, exist_ok=True)
(u / 'logs').mkdir(parents=True, exist_ok=True)
config = u / 'config.json'
if config.exists():
    raise SystemExit('Refusing to overwrite existing config.json')

cfg = {
 '$schema':'https://schema.freqtrade.io/schema.json',
 'bot_name':'btc_aud_ai_v3_paper',
 'trading_mode':'spot','max_open_trades':1,'stake_currency':'AUD',
 'stake_amount':50,'tradable_balance_ratio':0.20,
 'dry_run':True,'dry_run_wallet':1000,'fiat_display_currency':'AUD',
 'cancel_open_orders_on_exit':True,'force_entry_enable':False,
 'initial_state':'running','timeframe':'4h',
 'exchange':{
   'name':'kraken','key':'','secret':'',
   'ccxt_config':{'enableRateLimit':True},
   'ccxt_async_config':{'enableRateLimit':True,'rateLimit':3100},
   'pair_whitelist':['BTC/AUD'],'pair_blacklist':[]
 },
 'pairlists':[{'method':'StaticPairList'}],
 'entry_pricing':{'price_side':'other','use_order_book':True,'order_book_top':1},
 'exit_pricing':{'price_side':'other','use_order_book':True,'order_book_top':1},
 'unfilledtimeout':{'entry':10,'exit':10},
 'api_server':{
   'enabled':True,'listen_ip_address':'0.0.0.0','listen_port':8080,
   'verbosity':'error','enable_openapi':False,'CORS_origins':[],
   'username':'operator','password':secrets.token_urlsafe(32),
   'jwt_secret_key':secrets.token_hex(32),'ws_token':secrets.token_urlsafe(32)
 },
 'freqai':{
  'enabled':True,'identifier':'btc-aud-v3-nettrade-4h-72bars',
  'purge_old_models':3,
  'train_period_days':365,'backtest_period_days':7,
  'live_retrain_hours':168,'expired_hours':192,
  'feature_parameters':{
    'include_timeframes':['4h'],'include_corr_pairlist':[],
    'label_period_candles':72,'include_shifted_candles':2,
    'indicator_periods_candles':[14,28],
    'DI_threshold':0.9,'weight_factor':0.9
  },
  'data_split_parameters':{'test_size':0.2,'shuffle':False},
  'model_training_parameters':{
    'n_estimators':180,'learning_rate':0.035,
    'num_leaves':9,'min_child_samples':60,
    'reg_lambda':10.0,'colsample_bytree':0.85,
    'verbosity':-1,'random_state':42
  }
 },
 'internals':{'process_throttle_secs':5}
}
config.write_text(json.dumps(cfg,indent=2)+'\n')
config.chmod(0o600)
print('Created dry-run config. NOTE: 365-day training needs archived Kraken BTC/AUD history.')
print('Live trading is disabled. Use a separate explicitly reviewed config for live.')
