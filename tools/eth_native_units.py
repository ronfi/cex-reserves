#!/usr/bin/env python3
"""给已有快照补"原生 ETH 枚数"(报告 §3.2 与官方 PoR 自报 ETH 对照用):按 tools/cex_addresses.json 的 eth 清单逐址读 Blockscout coin_balance,
写入快照 JSON 各所 eth.native_eth(枚)与 eth.native_read_at。用法:python3 tools/eth_native_units.py data/cex_reserves_YYYY-MM-DD.json [--ex okx,gate]"""
import json, sys, time, datetime, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
from curl_cffi import requests as cr
ROOT = Path(__file__).resolve().parent.parent
snap = Path(sys.argv[1]); d = json.load(open(snap, encoding='utf8'))
A = json.load(open(ROOT / 'tools' / 'cex_addresses.json', encoding='utf8'))['exchanges']
exs = [e for e in (sys.argv[sys.argv.index('--ex') + 1].split(',') if '--ex' in sys.argv else A) if A[e].get('eth')]
def bal(a):
    for i in range(4):
        try:
            r = cr.get(f'https://eth.blockscout.com/api/v2/addresses/{a}', timeout=30, impersonate='chrome')
            if r.status_code == 200: return int(r.json().get('coin_balance') or 0) / 1e18
            if r.status_code == 404: return 0.0
        except Exception: pass
        time.sleep(2 * (i + 1))
    return None
for ex in exs:
    tot = 0.0; fail = []
    for a in A[ex]['eth']:
        b = bal(a)
        if b is None: fail.append(a)
        else: tot += b
        time.sleep(0.25)
    d.setdefault(ex, {}).setdefault('eth', {})['native_eth'] = tot; d[ex]['eth']['native_failed'] = fail
    d[ex]['eth']['native_read_at'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f'{ex:12s} 原生 ETH {tot:,.0f}(失败 {len(fail)})', flush=True)
json.dump(d, open(snap, 'w', encoding='utf8'), ensure_ascii=False, indent=1); print('写回', snap)
