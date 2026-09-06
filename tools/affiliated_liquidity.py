#!/usr/bin/env python3
"""关联币可变现性数据(报告 §8):各所主场交易对的 24h 成交额与 ±2% 盘口深度(各所公开行情接口,一手),
以及全市场 24h 成交额(CoinGecko /coins/markets 的 total_volume,⚠ 第三方,含所有上市场所)。
用法:python3 tools/affiliated_liquidity.py [--out data/affiliated_liquidity_YYYY-MM-DD.json]
"""
import json, sys, time, datetime, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
from curl_cffi import requests as cr
ROOT = Path(__file__).resolve().parent.parent
def get(u, **p):
    for i in range(6):  # CoinGecko 免费接口限流严格:429 时退避重试
        r = cr.get(u, params=p or None, timeout=30, impersonate='chrome')
        if r.status_code == 429: time.sleep(30 * (i + 1)); continue
        r.raise_for_status(); return r.json()
    r.raise_for_status()
def depth2(bids, asks):
    """±2% 盘口深度(美元):中间价上下 2% 内的挂单量之和。bids/asks 为 [(price, qty), …]。"""
    if not bids or not asks: return None, None
    mid = (bids[0][0] + asks[0][0]) / 2
    d = sum(p * q for p, q in bids if p >= mid * 0.98) + sum(p * q for p, q in asks if p <= mid * 1.02)
    return d, mid
# 各所接口:返回 (24h 成交额 USD, ±2% 深度 USD, 中间价)
def binance(sym):
    t = get('https://api.binance.com/api/v3/ticker/24hr', symbol=sym); b = get('https://api.binance.com/api/v3/depth', symbol=sym, limit=1000)
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['quoteVolume']), d, mid
def okx(inst):
    t = get('https://www.okx.com/api/v5/market/ticker', instId=inst)['data'][0]; b = get('https://www.okx.com/api/v5/market/books', instId=inst, sz=400)['data'][0]
    d, mid = depth2([(float(x[0]), float(x[1])) for x in b['bids']], [(float(x[0]), float(x[1])) for x in b['asks']]); return float(t['volCcy24h']), d, mid
def kucoin(sym):
    t = get('https://api.kucoin.com/api/v1/market/stats', symbol=sym)['data']; b = get('https://api.kucoin.com/api/v1/market/orderbook/level2_100', symbol=sym)['data']
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['volValue']), d, mid
def bybit(sym):
    t = get('https://api.bybit.com/v5/market/tickers', category='spot', symbol=sym)['result']['list'][0]; b = get('https://api.bybit.com/v5/market/orderbook', category='spot', symbol=sym, limit=200)['result']
    d, mid = depth2([(float(p), float(q)) for p, q in b['b']], [(float(p), float(q)) for p, q in b['a']]); return float(t['turnover24h']), d, mid
def mexc(sym):
    t = get('https://api.mexc.com/api/v3/ticker/24hr', symbol=sym); b = get('https://api.mexc.com/api/v3/depth', symbol=sym, limit=5000)
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['quoteVolume']), d, mid
def gate(pair):
    t = get('https://api.gateio.ws/api/v4/spot/tickers', currency_pair=pair)[0]; b = get('https://api.gateio.ws/api/v4/spot/order_book', currency_pair=pair, limit=1000)
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['quote_volume']), d, mid
def kraken(pair):
    t = list(get('https://api.kraken.com/0/public/Ticker', pair=pair)['result'].values())[0]; b = list(get('https://api.kraken.com/0/public/Depth', pair=pair, count=500)['result'].values())[0]
    px = float(t['c'][0]); d, mid = depth2([(float(x[0]), float(x[1])) for x in b['bids']], [(float(x[0]), float(x[1])) for x in b['asks']]); return float(t['v'][1]) * px, d, mid
def bitget(sym):
    t = get('https://api.bitget.com/api/v2/spot/market/tickers', symbol=sym)['data'][0]; b = get('https://api.bitget.com/api/v2/spot/market/orderbook', symbol=sym, limit=150)['data']
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['quoteVolume']), d, mid
def htx(sym):
    t = get('https://api.huobi.pro/market/detail/merged', symbol=sym)['tick']; b = get('https://api.huobi.pro/market/depth', symbol=sym, type='step0')['tick']
    d, mid = depth2([(float(p), float(q)) for p, q in b['bids']], [(float(p), float(q)) for p, q in b['asks']]); return float(t['vol']), d, mid
def bitfinex(sym):
    t = get(f'https://api-pub.bitfinex.com/v2/ticker/{sym}'); b = get(f'https://api-pub.bitfinex.com/v2/book/{sym}/P0', len=250)
    px = float(t[6]); bids = [(float(x[0]), float(x[2])) for x in b if float(x[2]) > 0]; asks = [(float(x[0]), -float(x[2])) for x in b if float(x[2]) < 0]
    d, mid = depth2(bids, asks); return float(t[7]) * px, d, mid

# ---- 30 日均日成交(各所日 K 线,取最近 30 个完整日,不含当日) ----
def _avg(vals):
    v = [x for x in vals if x is not None][-31:-1] if len(vals) > 30 else [x for x in vals if x is not None][:-1]
    return (sum(v) / len(v)) if v else None
def k_binance(sym):
    j = get('https://api.binance.com/api/v3/klines', symbol=sym, interval='1d', limit=31); return _avg([float(x[7]) for x in j])
def k_okx(inst):
    j = get('https://www.okx.com/api/v5/market/candles', instId=inst, bar='1D', limit=31)['data']; j = list(reversed(j)); return _avg([float(x[7]) for x in j])
def k_kucoin(sym):
    import time as _t; end = int(_t.time()); j = get('https://api.kucoin.com/api/v1/market/candles', type='1day', symbol=sym, startAt=end - 32 * 86400, endAt=end)['data']; j = list(reversed(j)); return _avg([float(x[6]) for x in j])
def k_bybit(sym):
    j = get('https://api.bybit.com/v5/market/kline', category='spot', symbol=sym, interval='D', limit=31)['result']['list']; j = list(reversed(j)); return _avg([float(x[6]) for x in j])
def k_mexc(sym):
    j = get('https://api.mexc.com/api/v3/klines', symbol=sym, interval='1d', limit=31); return _avg([float(x[7]) for x in j])
def k_gate(pair):
    j = get('https://api.gateio.ws/api/v4/spot/candlesticks', currency_pair=pair, interval='1d', limit=31); return _avg([float(x[1]) for x in j])
def k_kraken(pair):
    j = list(get('https://api.kraken.com/0/public/OHLC', pair=pair, interval=1440)['result'].values())[0]; return _avg([float(x[6]) * float(x[4]) for x in j])
def k_bitget(sym):
    j = get('https://api.bitget.com/api/v2/spot/market/candles', symbol=sym, granularity='1day', limit=31)['data']; return _avg([float(x[6]) for x in j])
def k_htx(sym):
    j = get('https://api.huobi.pro/market/history/kline', symbol=sym, period='1day', size=31)['data']; j = list(reversed(j)); return _avg([float(x['vol']) for x in j])
def k_bitfinex(sym):
    j = get(f'https://api-pub.bitfinex.com/v2/candles/trade:1D:{sym}/hist', limit=31); j = list(reversed(j)); return _avg([float(x[5]) * float(x[2]) for x in j])
KLINE = {binance: k_binance, okx: k_okx, kucoin: k_kucoin, bybit: k_bybit, mexc: k_mexc, gate: k_gate, kraken: k_kraken, bitget: k_bitget, htx: k_htx, bitfinex: k_bitfinex}
def cg_30d(cid):
    """CoinGecko 全市场 30 日均日成交(⚠ 第三方,含所有场所)"""
    j = get(f'https://api.coingecko.com/api/v3/coins/{cid}/market_chart', vs_currency='usd', days=31, interval='daily')
    vols = [v for _, v in j.get('total_volumes', [])]; return _avg(vols)

# 采样清单:币 → [(所, 函数, 交易对)];第一项为"主场"
VENUES = {
 'BNB': [('Binance', binance, 'BNBUSDT'), ('Bybit', bybit, 'BNBUSDT'), ('KuCoin', kucoin, 'BNB-USDT'), ('Gate', gate, 'BNB_USDT'), ('MEXC', mexc, 'BNBUSDT'), ('Bitget', bitget, 'BNBUSDT'), ('HTX', htx, 'bnbusdt'), ('Kraken', kraken, 'BNBUSD')],
 'LEO': [('Bitfinex', bitfinex, 'tLEOUSD'), ('Gate', gate, 'LEO_USDT'), ('KuCoin', kucoin, 'LEO-USDT'), ('MEXC', mexc, 'LEOUSDT'), ('Bitget', bitget, 'LEOUSDT')],
 'GT':  [('Gate', gate, 'GT_USDT'), ('MEXC', mexc, 'GTUSDT'), ('KuCoin', kucoin, 'GT-USDT'), ('Bitget', bitget, 'GTUSDT')],
 'KCS': [('KuCoin', kucoin, 'KCS-USDT'), ('Gate', gate, 'KCS_USDT'), ('MEXC', mexc, 'KCSUSDT'), ('Bitget', bitget, 'KCSUSDT')],
 'BGB': [('Bitget', bitget, 'BGBUSDT'), ('Gate', gate, 'BGB_USDT'), ('MEXC', mexc, 'BGBUSDT'), ('KuCoin', kucoin, 'BGB-USDT'), ('HTX', htx, 'bgbusdt')],
 'TRX': [('HTX', htx, 'trxusdt'), ('Binance', binance, 'TRXUSDT'), ('OKX', okx, 'TRX-USDT'), ('KuCoin', kucoin, 'TRX-USDT'), ('Bybit', bybit, 'TRXUSDT'), ('MEXC', mexc, 'TRXUSDT'), ('Gate', gate, 'TRX_USDT'), ('Kraken', kraken, 'TRXUSD'), ('Bitget', bitget, 'TRXUSDT'), ('Bitfinex', bitfinex, 'tTRXUSD')],
 'HTX': [('HTX', htx, 'htxusdt'), ('Bybit', bybit, 'HTXUSDT'), ('MEXC', mexc, 'HTXUSDT'), ('Gate', gate, 'HTX_USDT'), ('Bitget', bitget, 'HTXUSDT'), ('KuCoin', kucoin, 'HTX-USDT')],
}
CG = {'BNB': 'binancecoin', 'LEO': 'leo-token', 'GT': 'gatechain-token', 'KCS': 'kucoin-shares', 'BGB': 'bitget-token', 'TRX': 'tron', 'HTX': 'htx-dao'}
out = {'_meta': {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'script': 'tools/affiliated_liquidity.py',
                 'note': '主流所 = 各所公开行情接口的现货对:24h 成交额、近 30 个完整日的日均成交额(日 K 线)、±2% 盘口深度(一手;未上市的所记 error 跳过);全市场 = CoinGecko total_volume 与 market_chart 30 日均值(⚠ 第三方,含所有上市场所,不逐所核)'}}
try: cg = {c['id']: c for c in get('https://api.coingecko.com/api/v3/coins/markets', vs_currency='usd', ids=','.join(CG.values()))}
except Exception as e: cg = {}; print('CoinGecko coins/markets 不可用(限流),全市场 24h 留空:', str(e)[:60], flush=True)
for coin, vs in VENUES.items():
    rows = []
    for venue, fn, pair in vs:
        try:
            vol, d2, mid = fn(pair)
            try: v30 = KLINE[fn](pair)
            except Exception as e: v30 = None
            rows.append(dict(venue=venue, pair=pair, vol_24h_usd=vol, vol_30d_avg_usd=v30, depth2_usd=d2, mid=mid))
            print(f'{coin:4s} {venue:9s} {pair:10s} 24h ${vol/1e6:8.2f}M  30d均 ${(v30 or 0)/1e6:8.2f}M  ±2% ${(d2 or 0)/1e6:6.2f}M', flush=True)
        except Exception as e:
            rows.append(dict(venue=venue, pair=pair, error=str(e)[:120])); print(f'{coin:4s} {venue:9s} {pair:10s} ✗(未上市或接口失败) {str(e)[:60]}', flush=True)
        time.sleep(0.5)
    g = cg.get(CG[coin], {})
    try: m30 = cg_30d(CG[coin])
    except Exception as e: m30 = None
    time.sleep(15)
    ok = [r for r in rows if 'error' not in r]
    out[coin] = dict(venues=rows, home=rows[0]['venue'], venues_listed=len(ok), venues_vol_sum=sum(r.get('vol_24h_usd', 0) for r in ok), venues_vol30_sum=sum(r.get('vol_30d_avg_usd') or 0 for r in ok),
                     venues_depth2_sum=sum(r.get('depth2_usd') or 0 for r in ok), market_vol_24h_usd=g.get('total_volume'), market_vol_30d_avg_usd=m30, market_cap_usd=g.get('market_cap'), coingecko_updated=g.get('last_updated'))
    print(f'{coin:4s} 主流所({len(ok)}) 24h ${out[coin]["venues_vol_sum"]/1e6:,.1f}M  30d均 ${out[coin]["venues_vol30_sum"]/1e6:,.1f}M  ±2% ${out[coin]["venues_depth2_sum"]/1e6:,.2f}M | CoinGecko 全市场 24h ${(g.get("total_volume") or 0)/1e6:,.1f}M  30d均 ${(m30 or 0)/1e6:,.1f}M', flush=True)
p = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else ROOT / 'data' / f"affiliated_liquidity_{datetime.date.today():%Y-%m-%d}.json"
json.dump(out, open(p, 'w', encoding='utf8'), indent=1, ensure_ascii=False); print('写入', p)
