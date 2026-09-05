#!/usr/bin/env python3
"""抓取各所官方 PoR 页面/接口的自报数字(用户负债 / 交易所钱包,按币种),写入 data/por_<date>.json。
只用公开、无需登录的入口;页面为 JS 渲染时走页面自己调用的公开接口或 SSR 数据。用法:python3 tools/por_fetch.py [--out data/por_YYYY-MM-DD.json]
覆盖:OKX(静态页文本)、Bitget(公开 POST 接口)、KuCoin(页面 SSR 数据)、Gate(lastSnapshot 接口)、MEXC(stock_info 接口)、HTX(GitHub 快照 CSV,仅储备侧)。
未覆盖(需人工另存页面):Binance(页面有反爬挑战,接口未公开)、Bybit(接口未找到)、Crypto.com。"""
import re, json, sys, csv, io, time, datetime, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
from curl_cffi import requests as cr
ROOT = Path(__file__).resolve().parent.parent
UA = dict(timeout=40, impersonate='chrome')
def get(u): return cr.get(u, **UA)
def post(u, body): return cr.post(u, json=body, **UA)
def num(s): return float(str(s).replace(',', ''))
out = {'_meta': {'read_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'script': 'tools/por_fetch.py'}}

def okx():
    t = get('https://www.okx.com/proof-of-reserves').text
    t2 = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '|', t))
    coins = {}
    for m in re.finditer(r'\|([A-Za-z ]+)\|+([A-Z0-9]+)\|+(\d+)%\|+OKX account assets\|+([\d,\.]+)\|+OKX wallet assets\|+([\d,\.]+)\|+Exchange\|+([\d,\.]+)\|+Third-party custody\|+([\d,\.]+)', t2):
        coins[m.group(2)] = dict(users=num(m.group(4)), wallet=num(m.group(5)), exchange=num(m.group(6)), custody=num(m.group(7)), ratio=int(m.group(3)))
    snap = re.search(r'Our (\d+)(?:st|nd|rd|th) Proof of Reserves', t2)
    mon = re.search(r'Our \d+(?:st|nd|rd|th) Proof of Reserves[^|]*\|+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4})\|', t2)
    return dict(source='https://www.okx.com/proof-of-reserves(静态页文本)', snapshot=(mon.group(1) if mon else None), edition=(snap.group(1) if snap else None), coins=coins)

def bitget():
    base = 'https://www.bitget.com/v1/bill/proof/assets/public/'
    d = post(base + 'queryTotalReserveAmount', {}).json()['data'][0]
    det = post(base + 'queryPlatformReserveDetail', {'auditId': d['auditId']}).json()['data']['platformAssetDetailListList']
    coins = {x['coinName']: dict(users=x['customerTotalAmount'], wallet=sum(y['platformTotalAmount'] for y in x['platformTotalAssetList']),
                                 by_chain={y['chainName']: y['platformTotalAmount'] for y in x['platformTotalAssetList']}) for x in det}
    snap = datetime.datetime.fromtimestamp(int(d['snapshotTime']) / 1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return dict(source=base + '{queryTotalReserveAmount,queryPlatformReserveDetail}(POST)', snapshot=snap, audit_id=d['auditId'], total_ratio=d['totalReserveRatio'], coins=coins)

def kucoin():
    t = get('https://www.kucoin.com/proof-of-reserves').text
    j = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S).group(1))
    ir = j['props']['pageProps']['initialReserve']
    coins = {x['currency']: dict(users=float(x['userAsset']), wallet=float(x['walletAsset']), ratio=x.get('reserveRate')) for x in ir['reserveAsset']}
    snap = next((v for k, v in ir.items() if re.search(r'time|date', k, re.I) and not isinstance(v, (list, dict))), None)
    if snap is None:
        m = re.search(r'Based on data at ([0-9/ :]+ UTC[+-]\d+)', t); snap = m.group(1) if m else None
    if isinstance(snap, (int, float)) or (isinstance(snap, str) and snap.isdigit()):
        snap = datetime.datetime.fromtimestamp(int(snap) / 1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return dict(source='https://www.kucoin.com/proof-of-reserves(__NEXT_DATA__.initialReserve)', snapshot=snap, coins=coins)

def gate():
    d = get('https://www.gate.io/api/web/v1/bill/audit/lastSnapshot').json()['data']
    coins = {x['currency'].upper(): dict(users=num(x['customer_net_balances']), wallet=num(x['exchange_net_balances']) + num(x['third_net_balances']),
                                         exchange=num(x['exchange_net_balances']), custody=num(x['third_net_balances'])) for x in d['currency_data']}
    return dict(source='https://www.gate.io/api/web/v1/bill/audit/lastSnapshot', snapshot=d['snapshot_time'], total_ratio=d['total_reserve_rate'], coins=coins)

def mexc():
    dates = get('https://www.mexc.com/api/assetbussiness/asset/merkle/stock_info/snapshot_date').json()['data']
    d = get(f'https://www.mexc.com/api/assetbussiness/asset/merkle/stock_info?snapshotDate={dates[0]}').json()['data']
    coins = {x['currency']: dict(users=num(x['userSpotAsset']), wallet=num(x['walletTotalAsset']), ratio=num(x['stockRate'])) for x in d['details']}
    snap = datetime.datetime.fromtimestamp(int(d['snapshotDate']) / 1000, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return dict(source='https://www.mexc.com/api/assetbussiness/asset/merkle/stock_info', snapshot=snap, coins=coins)

def htx():
    """GitHub 月度快照 CSV:只有储备侧(coin, snapshot height, balance);用户负债只在页面上,页面有 JS 挑战,需人工另存。"""
    t = get('https://raw.githubusercontent.com/huobiapi/Tool-Node.js-VerifyAddress/main/snapshot/huobi_por.csv').text
    rows = list(csv.reader(io.StringIO(t)))[1:]
    coins = {}
    for row in rows:
        if len(row) < 3 or not row[0]: continue
        coin, height, bal = row[:3]
        if coin.upper().endswith('(ALL)'): coins[coin[:-5]] = dict(users=None, wallet=num(bal))
    commits = get('https://api.github.com/repos/huobiapi/Tool-Node.js-VerifyAddress/commits?path=snapshot/huobi_por.csv&per_page=1').json()
    msg = commits[0]['commit']['message'] if commits else ''
    m = re.search(r'snapshot\s*(\d{4})(\d{2})(\d{2})', msg)
    snap = f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else (commits[0]['commit']['committer']['date'] if commits else None)
    return dict(source='GitHub huobiapi/Tool-Node.js-VerifyAddress snapshot/huobi_por.csv(仅储备侧;负债侧需页面)', snapshot=snap, coins=coins)

for name, fn in [('okx', okx), ('bitget', bitget), ('kucoin', kucoin), ('gate', gate), ('mexc', mexc), ('htx', htx)]:
    try:
        out[name] = fn(); c = out[name]['coins'].get('BTC', {})
        print(f"{name:7s} 快照 {out[name].get('snapshot')} | BTC 用户 {c.get('users')} 钱包 {c.get('wallet')}", flush=True)
    except Exception as e:
        out[name] = {'error': str(e)[:200]}; print(name, '✗', str(e)[:120], flush=True)
    time.sleep(0.5)
# 人工快照(页面另存后手工登记):Binance、Bybit 等无公开接口者
manual = ROOT / 'data' / 'por_manual.json'
if manual.exists():
    for k, v in json.load(open(manual, encoding='utf8')).items():
        out.setdefault(k, v)
p = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else ROOT / 'data' / f"por_{datetime.date.today():%Y-%m-%d}.json"
json.dump(out, open(p, 'w', encoding='utf8'), indent=1, ensure_ascii=False); print('写入', p)
