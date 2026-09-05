#!/usr/bin/env python3
"""按提款地址统计信标链验证者数与余额(报告 §3.2 Bitstamp ETH 口径差的独立核法)。

质押在验证者里的 ETH 不在任何以太坊地址余额上,地址直读读不到;只能按"提款凭证 = 某地址"去信标链找验证者。
两步,均只用公共接口、无需 API key:
  1. Blockscout `/addresses/{a}/withdrawals` 翻页,收集出现过的验证者索引(已激活的验证者每轮扫描都会向提款地址打一笔,
     约 9 天一轮;连续 40 页无新索引即视为覆盖完整一轮);
  2. 近期激活或排队中的验证者还没有提款记录,但索引按存款先后分配,故从 --tail-from 起扫描注册表尾部到末尾补漏;
  最后用公共信标节点 `/eth/v1/beacon/states/head/validators?id=…` 按索引批量读余额与状态,只计当前提款凭证仍指向该地址者。
用法:python3 tools/beacon_validators.py 0x3262f13a… 0xf666814c… [--tail-from 2300000] [--out data/beacon.json]
"""
import argparse, json, time, warnings
warnings.filterwarnings('ignore')
from curl_cffi import requests as cr

BEACON = 'https://ethereum-beacon-api.publicnode.com'
BLOCKSCOUT = 'https://eth.blockscout.com/api/v2'

def get(u, tries=6):
    for i in range(tries):
        try:
            r = cr.get(u, timeout=60, impersonate='chrome')
            if r.status_code == 200:
                return r.json()
            print('  HTTP', r.status_code, u[-70:], flush=True)
        except Exception as e:
            print('  ✗', str(e)[:60], flush=True)
        time.sleep(5 * (i + 1))
    return None

def indices_from_withdrawals(addr, stale_pages=40):
    idx, params, pages, stale = set(), {}, 0, 0
    while True:
        q = '&'.join(f'{k}={v}' for k, v in params.items())
        j = get(f'{BLOCKSCOUT}/addresses/{addr}/withdrawals' + ('?' + q if q else ''))
        if j is None:
            raise SystemExit(f'提款记录读取失败:{addr}')
        before = len(idx)
        idx |= {x['validator_index'] for x in j.get('items', []) if x.get('validator_index') is not None}
        pages += 1
        stale = stale + 1 if len(idx) == before else 0
        params = j.get('next_page_params') or {}
        if not params or stale >= stale_pages:
            break
        time.sleep(0.35)
    print(f'{addr[:10]}… 提款记录:{len(idx)} 个索引(翻页 {pages})', flush=True)
    return idx

def scan_tail(addrs, start, step=200):
    found = {a: set() for a in addrs}
    i, empty = start, 0
    while True:
        j = get(f'{BEACON}/eth/v1/beacon/states/head/validators?id=' + ','.join(map(str, range(i, i + step))))
        if j is None:
            i += step; continue
        d = j.get('data', [])
        empty = empty + 1 if not d else 0
        if empty >= 3:
            break
        for v in d:
            c = '0x' + v['validator']['withdrawal_credentials'][-40:].lower()
            if c in found:
                found[c].add(int(v['index']))
        i += step; time.sleep(0.3)
    print(f'注册表尾扫 {start}–{i - 3 * step}:' + ', '.join(f'{a[:10]}… +{len(s)}' for a, s in found.items()), flush=True)
    return found

def balances(addr, idx):
    idx = sorted(idx); bal, n, st = 0.0, 0, {}
    for k in range(0, len(idx), 200):
        j = get(f'{BEACON}/eth/v1/beacon/states/head/validators?id=' + ','.join(map(str, idx[k:k + 200])))
        if j is None:
            raise SystemExit('余额批读取失败')
        for d in j.get('data', []):
            if d['validator']['withdrawal_credentials'][-40:].lower() != addr[2:].lower():
                continue
            bal += int(d['balance']) / 1e9; n += 1; st[d['status']] = st.get(d['status'], 0) + 1
        time.sleep(0.4)
    return n, bal, st

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('addresses', nargs='+')
    ap.add_argument('--tail-from', type=int, default=2_300_000, help='注册表尾扫起点索引(应低于最近 ~2 周激活的验证者索引)')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    addrs = [x.lower() for x in a.addresses]
    sets = {x: indices_from_withdrawals(x) for x in addrs}
    for x, s in scan_tail(addrs, a.tail_from).items():
        sets[x] |= s
    out, tv, tb = {}, 0, 0.0
    for x in addrs:
        n, bal, st = balances(x, sets[x])
        out[x] = dict(validators=n, balance_eth=round(bal, 3), status=st)
        tv += n; tb += bal
        print(f'== {x}: 验证者 {n},余额 {bal:,.0f} ETH,状态 {st}', flush=True)
    out['_total'] = dict(validators=tv, balance_eth=round(tb, 3), read_at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    print('合计', json.dumps(out['_total']))
    if a.out:
        json.dump(out, open(a.out, 'w'), indent=1)
