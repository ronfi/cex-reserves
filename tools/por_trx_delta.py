#!/usr/bin/env python3
"""Poloniex 官方 PoR 快照里的 TRX 地址:快照余额 vs 链上现值,逐址列出,并追踪快照日后的 TRX 转出去向。
用法:python3 tools/por_trx_delta.py [--since 2026-08-01]
数据源:GitHub poloniex/tools-nodejs-address-verify(master)snapshot/poloniex_por.csv;trongrid getaccount / transactions;JustLend jSTRX.underlying() 取 sTRX 合约。
"""
import csv, io, json, sys, time, hashlib, datetime as dt
import warnings; warnings.filterwarnings('ignore')
from curl_cffi import requests as cr
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58dec(s):
    n = 0
    for ch in s: n = n * 58 + B58.index(ch)
    return n.to_bytes(25, 'big')[:-4].hex()
def b58enc(h):
    b = bytes.fromhex(h); ck = hashlib.sha256(hashlib.sha256(b).digest()).digest()[:4]; x = int.from_bytes(b + ck, 'big'); s = ''
    while x: x, r = divmod(x, 58); s = B58[r] + s
    return s
def get(u):
    for i in range(4):
        try:
            r = cr.get(u, timeout=25, impersonate='chrome')
            if r.status_code == 200: return r.json()
        except Exception: pass
        time.sleep(2 * (i + 1))
    return None
def acct(a):
    for k in range(4):
        try:
            j = cr.post('https://api.trongrid.io/wallet/getaccount', json={'address': b58dec(a), 'visible': False}, timeout=20, impersonate='chrome').json()
            if 'Error' in j: raise RuntimeError(j['Error'])
            fz = (sum(x.get('frozen_balance', 0) for x in j.get('frozen', [])) + sum((x.get('amount') or 0) for x in j.get('frozenV2', []))) / 1e6
            dl = ((j.get('delegated_frozenV2_balance_for_bandwidth') or 0) + (j.get('account_resource', {}).get('delegated_frozenV2_balance_for_energy') or 0) + sum((x.get('unfreeze_amount') or 0) for x in j.get('unfrozenV2', []))) / 1e6
            return j.get('balance', 0) / 1e6, fz, dl
        except Exception: time.sleep(2 * (k + 1))
    return None, None, None
def trc20(a, contract, dec):
    for u in ('https://api.trongrid.io/jsonrpc', 'https://tron-rpc.publicnode.com'):
        try:
            r = cr.post(u, json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': '0x' + b58dec(contract)[2:], 'data': '0x70a08231' + b58dec(a)[2:].zfill(64)}, 'latest']}, timeout=20, impersonate='chrome').json()
            if r.get('result') not in (None, '0x'): return int(r['result'], 16) / 10 ** dec
        except Exception: pass
    return None
def call_addr(contract, sel):
    r = cr.post('https://api.trongrid.io/jsonrpc', json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': '0x' + b58dec(contract)[2:], 'data': sel}, 'latest']}, timeout=20, impersonate='chrome').json()
    return b58enc('41' + r['result'][-40:])
since = sys.argv[sys.argv.index('--since') + 1] if '--since' in sys.argv else '2026-08-01'
txt = cr.get('https://raw.githubusercontent.com/poloniex/tools-nodejs-address-verify/master/snapshot/poloniex_por.csv', timeout=30, impersonate='chrome').text.lstrip('﻿')
lines = txt.splitlines(); i2 = next(i for i, l in enumerate(lines) if l.startswith('coin,address'))
det = list(csv.DictReader(io.StringIO('\n'.join(lines[i2:]))))
def _f(x):
    try: return float(x)
    except Exception: return 0.0
rows = [(r['address'], _f(r['balance'])) for r in det if r['coin'] == 'TRX' and r['address'].startswith('T')]
strx_rows = {r['address']: _f(r['balance']) for r in det if r['coin'] == 'sTRX'}
STRX = call_addr('TJQ9rbVe9ei3nNtyGgBL22Fuu2xYjZaLAQ', '0x6f307dc3')  # jSTRX.underlying()
STRX_DEC = int(cr.post('https://api.trongrid.io/jsonrpc', json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': '0x' + b58dec(STRX)[2:], 'data': '0x313ce567'}, 'latest']}, timeout=20, impersonate='chrome').json()['result'], 16)
print(f'# Poloniex PoR TRX 地址:快照 vs 链上({dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M")} UTC);sTRX 合约 {STRX}\n')
print('| 地址 | 快照 TRX | 可用 | 自持质押 | 委托质押/解押中 | 合计 | 变动 | sTRX 现值(快照) | 快照日后 TRX 转出(≥1M) |')
print('|---|---|---|---|---|---|---|---|---|')
tot_s = tot_n = tot_strx = 0.0
ms = int(dt.datetime.fromisoformat(since).replace(tzinfo=dt.timezone.utc).timestamp() * 1000)
for a, snap in rows:
    bal, fz, dl = acct(a); time.sleep(1.2)
    st = trc20(a, STRX, STRX_DEC); time.sleep(0.6)
    outs = {}; url = f'https://api.trongrid.io/v1/accounts/{a}/transactions?only_from=true&limit=200&min_timestamp={ms}'; p = 0
    while url and p < 5:
        j = get(url)
        if not j: break
        for tx in j.get('data', []):
            for c in tx.get('raw_data', {}).get('contract', []):
                if c.get('type') == 'TransferContract':
                    v = c['parameter']['value']; amt = v.get('amount', 0) / 1e6
                    if amt >= 1e6:
                        to = v.get('to_address'); to = b58enc(to) if len(to) == 42 else to; outs[to] = outs.get(to, 0) + amt
        url = j.get('meta', {}).get('links', {}).get('next'); p += 1; time.sleep(1.5)
    dest = '; '.join(f'{k[:8]}… {v/1e6:.1f}M' for k, v in sorted(outs.items(), key=lambda x: -x[1])[:3]) or '—'
    tot = (bal or 0) + (fz or 0) + (dl or 0)
    tot_s += snap; tot_n += tot; tot_strx += (st or 0)
    print(f'| [`{a[:10]}…`](https://tronscan.org/#/address/{a}) | {snap/1e6:,.2f}M | {(bal or 0)/1e6:,.2f}M | {(fz or 0)/1e6:,.2f}M | {(dl or 0)/1e6:,.2f}M | {tot/1e6:,.2f}M | {(tot/snap-1)*100 if snap else 0:+.0f}% | {(st or 0)/1e6:,.2f}M({strx_rows.get(a,0)/1e6:,.0f}M) | {dest} |')
print(f'| **合计** | **{tot_s/1e6:,.2f}M** | | | | **{tot_n/1e6:,.2f}M** | **{(tot_n/tot_s-1)*100:+.0f}%** | **{tot_strx/1e6:,.2f}M** | |')
