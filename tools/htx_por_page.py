#!/usr/bin/env python3
"""解析 HTX 官方 PoR 页面的另存快照(.mhtml/.html)→ 结构化自报数,写入 data/por_manual.json 的 htx_page。

为什么需要它:HTX 的储备侧在 GitHub CSV 上可自动取(tools/por_fetch.py),但
  ① 负债侧只在页面上,页面有 JS 挑战,需人工另存;
  ② GitHub CSV 的推送比页面快照晚约 11 天(如 20260801 的 CSV 在 08-12 才推)。
⇒ 若把"页面的新负债"与"CSV 的旧储备"放进同一格,就是拿两个快照日的数相比。
   本脚本把整页(负债 + 储备 + 交易所钱包 + 第三方托管)按同一快照日一次性登记。

用法:python3 tools/htx_por_page.py PoR-Snapshot/HTX-YYYYMMDD.mhtml [--write]
"""
import re, sys, json, email, datetime, os
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SRC = sys.argv[1]

raw = open(SRC, 'rb').read()
if raw[:5] == b'From:':                       # Blink 另存的 mhtml
    parts = [p for p in email.message_from_bytes(raw).walk() if p.get_content_type() == 'text/html']
    html = max((p.get_payload(decode=True).decode('utf8', 'ignore') for p in parts), key=len)
else:
    html = raw.decode('utf8', 'ignore')
txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)
txt = re.sub(r'\n{2,}', '\n', re.sub(r'<[^>]+>', '\n', txt)).strip()

num = lambda s: float(s.replace(',', ''))
snap = re.search(r'Audit Time \(UTC\+8\)\s*\n\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})', txt)
if not snap:
    raise SystemExit('未找到快照日(Audit Time)——页面结构可能已变,勿猜')
snapshot = f'{snap.group(1)}T{snap.group(2)}+08:00'

# 主表:每个币一段 "COIN / Ratio / …/ NN% / User Balance / x / HTX Balance / y / Exchange Wallets / z [/ Custodial Wallets / w]"
coins = {}
for m in re.finditer(r'\n(BTC|ETH|TRX|USDs|HTX|XRP|DOGE|SOL)\s*\n\s*Ratio\s*\n(.{0,4000}?)'
                     r'User Balance\s*\n\s*([\d,]+)\s*\nHTX Balance\s*\n\s*([\d,]+)\s*\n'
                     r'Exchange Wallets\s*\n\s*([\d,]+)(?:\s*\nCustodial Wallets\s*\n\s*([\d,]+))?', txt, re.S):
    coin, mid, u, w, ex, cu = m.groups()
    ratio = re.search(r'(\d+)%', mid)
    coins[coin] = dict(users=num(u), wallet=num(w), exchange=num(ex),
                       custody=num(cu) if cu else 0.0, ratio=int(ratio.group(1)) if ratio else None)

# USDs 明细表:Coin / User Balance / Exchange Wallets / Custodial Wallets(托管为 "--" 时记 0)
usds = {}
i = txt.find('\nCoin\n')   # ⚠ 不能用 find('Coin'):导航栏里有 "Coin-M"
blk = txt[i:i + 900] if i > 0 else ''
if blk:
    for m in re.finditer(r'\n\s*(USDT|USDC|USDS|U|USDD)\s*\n\s*([\d,]+)\s*\n\s*([\d,]+)\s*\n\s*([\d,]+|--)', blk):
        c, u, ex, cu = m.groups()
        usds[c] = dict(users=num(u), exchange=num(ex), custody=0.0 if cu == '--' else num(cu))
        usds[c]['wallet'] = usds[c]['exchange'] + usds[c]['custody']
if usds and 'USDs' in coins:      # 明细合计须与主行对上,否则解析漏了某一行
    for f in ('users', 'exchange', 'custody'):
        a, b = sum(v[f] for v in usds.values()), coins['USDs'][f]
        assert abs(a - b) / max(b, 1) < 0.005, f'USDs 明细 {f} 合计 {a:,.0f} 与主行 {b:,.0f} 不符'
if not coins or 'BTC' not in coins or 'USDs' not in coins:
    raise SystemExit('主表解析为空——页面结构可能已变,勿猜')

# 计价:快照日当日收盘(币安日线),稳定币按 $1 并显式标注,HTX 币用 CoinGecko
day = snap.group(1)
def kline(sym):
    t0 = int(datetime.datetime.strptime(day, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    r = requests.get('https://api.binance.com/api/v3/klines',
                     params=dict(symbol=sym, interval='1d', startTime=t0, limit=1), timeout=30).json()
    return float(r[0][4])
px = {c: kline(c + 'USDT') for c in ('BTC', 'ETH', 'TRX', 'XRP', 'DOGE', 'SOL')}
px |= {c: 1.0 for c in ('USDT', 'USDC', 'USDS', 'U', 'USDD', 'USDs')}   # ⚠ 稳定币按面值,不按市价
try:
    px['HTX'] = requests.get('https://api.coingecko.com/api/v3/simple/price',
                             params=dict(ids='htx-dao', vs_currencies='usd'), timeout=30).json()['htx-dao']['usd']
except Exception as e:
    px['HTX'] = None; print('⚠ HTX 币价未取到:', str(e)[:80])

usd = lambda k, f: sum((coins[c][f] * px[c]) for c in coins if px.get(c)) if k == 'all' else None
tot_u = sum(coins[c]['users'] * px[c] for c in coins if px.get(c))
tot_w = sum(coins[c]['wallet'] * px[c] for c in coins if px.get(c))
tot_cu = sum(coins[c]['custody'] * px[c] for c in coins if px.get(c))
tot_ex = sum(coins[c]['exchange'] * px[c] for c in coins if px.get(c))

print(f'快照 {snapshot}  来源 {os.path.basename(SRC)}')
print(f'{"币":6s}{"比率":>6s}{"用户负债":>22s}{"自报储备":>22s}{"交易所钱包":>22s}{"第三方托管":>20s}')
for c, d in coins.items():
    print(f'{c:6s}{(str(d["ratio"])+"%"):>6s}{d["users"]:>22,.0f}{d["wallet"]:>22,.0f}{d["exchange"]:>22,.0f}{d["custody"]:>20,.0f}')
print('USDs 明细:', {k: f"{v['users']:,.0f}/{v['exchange']:,.0f}/{v['custody']:,.0f}" for k, v in usds.items()})
print(f'\n计价({day} 币安日收;稳定币按 $1;HTX ${px["HTX"]}):')
print(f'  用户负债 ${tot_u/1e9:.2f}B | 自报储备 ${tot_w/1e9:.2f}B | 第三方托管占储备 {tot_cu/tot_w:.1%} | 仅自有钱包 ÷ 负债 {tot_ex/tot_u:.1%}')
for c in coins:
    if px.get(c): print(f'    {c:5s} 占储备 {coins[c]["wallet"]*px[c]/tot_w:6.1%}')

if '--write' in sys.argv:
    f = ROOT + 'data/por_manual.json'
    d = json.load(open(f, encoding='utf8'))
    d.pop('htx_liabilities', None)          # 旧结构只有负债侧,被本条完全取代
    d['htx_page'] = dict(
        source='HTX 官方 PoR 页面另存快照(负债与储备同页同快照日;GitHub CSV 的储备侧比页面晚约 11 天,故不混用)',
        snapshot=snapshot, priced_at=day, prices=px,
        usd=dict(users=tot_u, wallet=tot_w, custody=tot_cu, exchange=tot_ex),
        coins={c: {k: v for k, v in d0.items()} for c, d0 in coins.items()}, usds=usds)
    json.dump(d, open(f, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('\n已写入 data/por_manual.json 的 htx_page(并移除旧的 htx_liabilities)')
