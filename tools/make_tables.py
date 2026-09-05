#!/usr/bin/env python3
"""从 data/cex_reserves_<date>.json 生成报告 §3 的对账表(markdown)。用法:python3 tools/make_tables.py data/cex_reserves_2026-09-03.json [--lang en]"""
import json, sys, re
LANG = 'en' if '--lang' in sys.argv and sys.argv[sys.argv.index('--lang') + 1] == 'en' else 'zh'
r = json.load(open([a for a in sys.argv[1:] if a.endswith('.json')][0], encoding='utf8'))
S = {  # 表头与标题(两种语言,数据行相同)
 'zh': dict(h31='### 3.1 BTC 链(mempool.space 直读 vs 聚合器;差值 ≤1% 绿、>5% 红)\n', t31='| 所 | 公布地址(读到/总) | 直读 BTC | 聚合器 BTC(≈) | 差 | PoR 自报 BTC:用户 / 钱包(快照日) | 直读 − 自报钱包 |',
  h32='### 3.2 ETH 链(Blockscout 全资产直读 vs 聚合器;"聚合器口径"列剔 USDD/HBTC/aEthUSDT;覆盖 95–105% 绿、<90% 或 >110% 红)\n', t32='| 所 | 地址数 | 全资产直读 | 聚合器口径直读 | 聚合器 | 覆盖 | 失败地址 | 直读原生 ETH | PoR 自报 ETH:用户 / 钱包(快照日) | 直读原生 − 自报钱包 |', lock=' + 锁仓 ',
  h33='### 3.3 Tron 链(trongrid `getaccount` 含四项质押 + USDT-TRC20 直读)\n', t33='| 所 | 地址数 | TRX 可用 | TRX 质押中 | USDT-TRC20 | PoR 自报 TRX:用户 / 钱包 | 直读 TRX − 自报钱包 | PoR 自报 USDT(全链):用户 / 钱包 |'),
 'en': dict(h31='### 3.1 BTC chain (mempool.space direct read vs aggregator; difference ≤1% green, >5% red)\n', t31='| Exchange | Addresses (read/total) | Direct BTC | Aggregator BTC | Diff | PoR BTC: users / wallets (snapshot) | Direct − PoR wallets |',
  h32='### 3.2 ETH chain (Blockscout all-asset direct read vs aggregator; the "aggregator-caliber" column excludes USDD/HBTC/aEthUSDT; coverage 95–105% green, <90% or >110% red)\n', t32='| Exchange | Addresses | All-asset read | Aggregator-caliber read | Aggregator | Coverage | Failed | Direct native ETH | PoR ETH: users / wallets (snapshot) | Direct native − PoR wallets |', lock=' + lock ',
  h33='### 3.3 Tron chain (trongrid `getaccount` with four staking buckets + direct USDT-TRC20 read)\n', t33='| Exchange | Addresses | TRX available | TRX staked | USDT-TRC20 | PoR TRX: users / wallets | Direct TRX − PoR wallets | PoR USDT (all chains): users / wallets |'),
}[LANG]
NAME = {'binance-cex': 'Binance', 'okx': 'OKX', 'bitfinex': 'Bitfinex', 'bybit': 'Bybit', 'gate': 'Gate', 'bitget': 'Bitget', 'mexc': 'MEXC', 'gemini': 'Gemini', 'deribit': 'Deribit', 'htx': 'HTX', 'kucoin': 'KuCoin', 'crypto-com': 'Crypto.com', 'bitstamp': 'Bitstamp'}
ORDER = ['binance-cex', 'okx', 'bitfinex', 'bybit', 'gate', 'bitget', 'mexc', 'gemini', 'deribit', 'htx', 'kucoin', 'crypto-com', 'bitstamp']
import glob, os, datetime
def _por_load():
    fs = [f for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'por_*.json'))) if 'manual' not in f]
    return json.load(open(fs[-1], encoding='utf8')) if fs else {}
_POR = _por_load()
def _day(s):
    if not s: return '?'
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', str(s))
    if m: return f'{m.group(2)}-{m.group(3)}'
    MON = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})', str(s)); return f'{m.group(2)}-{MON[m.group(1)]}' if m else str(s)[:8]
def por(ex, coin):
    """各所官方 PoR 自报:(用户, 钱包, 快照日) 或 None。来源 data/por_<date>.json(tools/por_fetch.py 抓取 + data/por_manual.json 人工登记)。"""
    key = 'binance' if ex == 'binance-cex' else ex
    e = _POR.get(key) or {}; c = (e.get('coins') or {}).get(coin)
    if not c: return None
    users = c.get('users')
    if users is None and key == 'htx': users = (((_POR.get('htx_liabilities') or {}).get('coins') or {}).get(coin) or {}).get('users')
    return (users, c.get('wallet'), _day(e.get('snapshot')))
def por_cell(ex, coin, scale=1, fmt='{:,.0f}'):
    x = por(ex, coin)
    if not x: return '—'
    u = fmt.format(x[0]/scale) if x[0] is not None else '?'
    w = fmt.format(x[1]/scale) if x[1] is not None else '?'
    return f'{u} / {w}({x[2]})'
POR_BTC = {ex: por(ex, 'BTC') for ex in ORDER if por(ex, 'BTC')}
REASON_TRX = {'zh': {'gate': 'DefiLlama-Adapters 清单 11 址不是页面全部钱包(Gate 未公布 TRX 地址)'}, 'en': {'gate': 'the 11-address DefiLlama-Adapters list is not every wallet on the page (Gate publishes no TRX addresses)'}}[LANG]
REASON = {  # 直读 ÷ 自报钱包 偏离 >5% 时的原因(两种语言);没有原因的不写
 'zh': {'gate': 'DefiLlama-Adapters清单 13 址不是页面全部钱包(Gate 未公布 BTC 地址)', 'bitget': '适配器 19 址不是页面全部钱包;页面钱包含 BSC/Lightning 等链 535 枚', 'htx': '自报钱包含 BTC-TRC20 10,399 + 托管 1,689 + BTC-SOL/jWBTC 175;原生 8,209 vs 直读 +2%', 'bybit': '新闻稿快照 07-23 vs 直读 09-04'},
 'en': {'gate': 'the 13-address DefiLlama-Adapters list is not every wallet on the page (Gate publishes no BTC addresses)', 'bitget': 'the 19-address adapter list is not every wallet on the page; page wallets include 535 BTC on BSC/Lightning etc.', 'htx': 'reported wallet includes BTC-TRC20 10,399 + custody 1,689 + BTC-SOL/jWBTC 175; native 8,209 vs direct read +2%', 'bybit': 'press-release snapshot 07-23 vs direct read 09-04'},
}[LANG]
btcpx = r['binance-cex']['llama']['Bitcoin'] / r['binance-cex']['btc']['btc']  # 用币安行反推聚合器计价
out = []
out.append(S['h31'])
out.append(S['t31'])
out.append('|---|---|---|---|---|---|---|')
for ex in ORDER:
    b = r[ex].get('btc'); lb = r[ex]['llama'].get('Bitcoin')
    if not b: continue
    n_ok = b['n'] - len(b['failed']); la = lb / btcpx if lb else None
    if la:
        d = (b['btc']/la-1)*100
        diff = f'<span class="ok">{d:+.1f}%</span>' if abs(d) <= 1 else (f'<mark class="r">{d:+.1f}%</mark>' if abs(d) > 5 else f'{d:+.1f}%')
    else:
        diff = '—'
    pb = POR_BTC.get(ex); porc = (f"{pb[0]:,.0f} / {pb[1]:,.0f}({pb[2]})" if pb[0] is not None else f"? / {pb[1]:,.0f}({pb[2]})") if pb else '—'
    if pb and pb[1]:
        dv = (b['btc']/pb[1]-1)*100; rs = REASON.get(ex, '')
        dcell = (f'<mark class="r">{dv:+.1f}%</mark>' if abs(dv) > 5 else f'{dv:+.1f}%') + (f'({rs})' if rs and abs(dv) > 5 else '')
    else: dcell = '—'
    out.append(f"| {NAME[ex]} | {n_ok}/{b['n']} | {b['btc']:,.0f} | {f'{la:,.0f}' if la else '—'} | {diff} | {porc} | {dcell} |")
out.append('\n@@ETH@@\n' + S['h32'])
out.append(S['t32'])
out.append('|---|---|---|---|---|---|---|---|---|---|')
ETH_CALIBER_NOTE = {'bitstamp'}  # 聚合器把信标链质押计入,本报告不计;差额为口径差
for ex in ORDER:
    e = r[ex].get('eth'); ll = r[ex]['llama'].get('Ethereum')
    if not e: continue
    lock = r[ex].get('eth_lock', {}); full = e['total_usd'] + lock.get('total_usd', 0); cal = e.get('total_usd_llama_caliber', e['total_usd']) + lock.get('total_usd_llama_caliber', 0)
    n = f"{e['n']}" + (f"{S['lock']}{lock['n']}" if lock else '')
    cov = cal/ll*100
    covs = f'<span class="ok">{cov:.0f}%</span>' if 95 <= cov <= 105 else (f'<mark class="r">{cov:.0f}%</mark>' if cov < 90 or cov > 110 else f'{cov:.0f}%')
    if ex in ETH_CALIBER_NOTE: covs = f'<mark class="n">{cov:.0f}%*</mark>'  # 口径差(见表下 * 注),不按红标规则判
    ne = e.get('native_eth'); pe = por(ex, 'ETH')
    ne_cell = f"{ne:,.0f}" if ne is not None else '—'
    ne_diff = (f"{(ne/pe[1]-1)*100:+.0f}%" if (ne is not None and pe and pe[1]) else '—')  # 自报钱包为全链口径,差值只作参照,不着色
    out.append(f"| {NAME[ex]} | {n} | ${full/1e9:.2f}B | ${cal/1e9:.2f}B | ${ll/1e9:.2f}B | {covs} | {len(e['failed'])} | {ne_cell} | {por_cell(ex, 'ETH')} | {ne_diff} |")
out.append('\n@@TRON@@\n' + S['h33'])
out.append(S['t33'])
out.append('|---|---|---|---|---|---|---|---|')
for ex in ORDER:
    t = r[ex].get('tron')
    if not t: continue
    pt = por(ex, 'TRX'); trx_diff = '—'
    if pt and pt[1]:
        dv = ((t['trx_available'] + t['trx_frozen'])/pt[1]-1)*100; rs = REASON_TRX.get(ex, '')
        trx_diff = (f'<mark class="r">{dv:+.1f}%</mark>' if abs(dv) > 5 else f'{dv:+.1f}%') + (f'({rs})' if rs and abs(dv) > 5 else '')
    out.append(f"| {NAME[ex]} | {t['n']} | {t['trx_available']/1e6:,.0f}M | {t['trx_frozen']/1e6:,.0f}M | {t['usdt_trc20']/1e6:,.1f}M | {por_cell(ex, 'TRX', 1e6, '{:,.0f}M')} | {trx_diff} | {por_cell(ex, 'USDT', 1e6, '{:,.0f}M')} |")
print('\n'.join(out))
