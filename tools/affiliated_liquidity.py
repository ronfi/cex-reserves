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
    r = cr.get(u, params=p or None, timeout=30, impersonate='chrome'); r.raise_for_status(); return r.json()
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
# 采样清单:币 → [(所, 函数, 交易对)];第一项为"主场"
VENUES = {
 'BNB': [('Binance', binance, 'BNBUSDT')],
 'LEO': [('Bitfinex', bitfinex, 'tLEOUSD')],
 'GT':  [('Gate', gate, 'GT_USDT')],
 'KCS': [('KuCoin', kucoin, 'KCS-USDT')],
 'BGB': [('Bitget', bitget, 'BGBUSDT')],
 'TRX': [('HTX', htx, 'trxusdt'), ('Binance', binance, 'TRXUSDT'), ('OKX', okx, 'TRX-USDT'), ('KuCoin', kucoin, 'TRX-USDT'), ('Bybit', bybit, 'TRXUSDT'), ('MEXC', mexc, 'TRXUSDT'), ('Gate', gate, 'TRX_USDT'), ('Kraken', kraken, 'TRXUSD'), ('Bitget', bitget, 'TRXUSDT'), ('Bitfinex', bitfinex, 'tTRXUSD')],
 'HTX': [('HTX', htx, 'htxusdt'), ('Bybit', bybit, 'HTXUSDT'), ('MEXC', mexc, 'HTXUSDT'), ('Gate', gate, 'HTX_USDT'), ('Bitget', bitget, 'HTXUSDT'), ('KuCoin', kucoin, 'HTX-USDT')],
}
CG = {'BNB': 'binancecoin', 'LEO': 'leo-token', 'GT': 'gatechain-token', 'KCS': 'kucoin-shares', 'BGB': 'bitget-token', 'TRX': 'tron', 'HTX': 'htx-dao'}
out = {'_meta': {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'script': 'tools/affiliated_liquidity.py',
                 'note': '主场/各所 = 该所公开行情接口的现货对 24h 成交额(计价币)与 ±2% 盘口深度(一手);全市场 = CoinGecko coins/markets total_volume(⚠ 第三方,含所有上市场所)'}}
cg = {c['id']: c for c in get('https://api.coingecko.com/api/v3/coins/markets', vs_currency='usd', ids=','.join(CG.values()))}
for coin, vs in VENUES.items():
    rows = []
    for venue, fn, pair in vs:
        try:
            vol, d2, mid = fn(pair); rows.append(dict(venue=venue, pair=pair, vol_24h_usd=vol, depth2_usd=d2, mid=mid))
            print(f'{coin:4s} {venue:9s} {pair:10s} 24h ${vol/1e6:8.2f}M  ±2% ${(d2 or 0)/1e6:6.2f}M', flush=True)
        except Exception as e:
            rows.append(dict(venue=venue, pair=pair, error=str(e)[:120])); print(f'{coin:4s} {venue:9s} {pair:10s} ✗ {str(e)[:80]}', flush=True)
        time.sleep(0.4)
    g = cg.get(CG[coin], {})
    out[coin] = dict(venues=rows, home=rows[0]['venue'], venues_vol_sum=sum(r.get('vol_24h_usd', 0) for r in rows), venues_depth2_sum=sum(r.get('depth2_usd') or 0 for r in rows),
                     market_vol_24h_usd=g.get('total_volume'), market_cap_usd=g.get('market_cap'), coingecko_updated=g.get('last_updated'))
    print(f'{coin:4s} 采样所合计 24h ${out[coin]["venues_vol_sum"]/1e6:,.1f}M  ±2% ${out[coin]["venues_depth2_sum"]/1e6:,.2f}M | 全市场(CoinGecko) ${(g.get("total_volume") or 0)/1e6:,.1f}M', flush=True)
p = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else ROOT / 'data' / f"affiliated_liquidity_{datetime.date.today():%Y-%m-%d}.json"
json.dump(out, open(p, 'w', encoding='utf8'), indent=1, ensure_ascii=False); print('写入', p)
