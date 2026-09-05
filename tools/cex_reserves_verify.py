#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交易所储备链上直读 —— 交易所储备核查(公开版)的可复现脚本。

用法:
  python3 tools/cex_reserves_verify.py --chain eth|btc|tron|all [--ex okx,gate] [--out 数据交付/cex_reserves_YYYY-MM-DD.json]
  python3 tools/cex_reserves_verify.py --refresh-addresses   # 重新拉 Binance PoR / lockinfo 与 Bitstamp 钱包接口,更新 tools/cex_addresses.json

读法(与报告 §3 一致):
  ETH 链:每个地址读原生 ETH + 全部有报价的 ERC20(Blockscout eth.blockscout.com /api/v2,含 exchange_rate);
         Blockscout 无报价/报价偏低的平台币(KCS/GT/BGB/LEO/HT)改为链上 balanceOf 直读 × DefiLlama coins 价;
         每个地址的失败/重试逐条记录到输出 JSON 的 failed 列表,可用 --retry-failed 单独补读。
  BTC 链:mempool.space /api/address(funded − spent)。
  Tron 链:trongrid wallet/getaccount(可用 + 冻结:V1/V2 自持 + 委托出去的质押 + 解押队列)+ USDT-TRC20 balanceOf(JSON-RPC eth_call)。
  对照:DefiLlama api.llama.fi/protocol/{slug} 的 currentChainTvls(Ethereum/Bitcoin/Tron)。

🔴 已知坑(均已在本脚本内规避):
  - JSON-RPC 批量 eth_call(一次打包几十个调用)在公共节点上会被静默截断,总额只剩 40% ⇒ 本脚本只用单调用。
  - Blockscout 对 Binance 热钱包偶发 429/5xx ⇒ 指数退避 + 失败清单 + --retry-failed。
  - DefiLlama 的 Binance 以太坊数含锚定代币抵押储备(lockinfo 地址),本脚本单列为 binance-lock,不并入用户储备。
  - Tron `eth_getBalance` 不含质押冻结,必须用 getaccount;且 getaccount 的 `balance + frozenV2` 仍不含【委托给他址的质押】(delegated_frozenV2_*),漏读会把 Poloniex 的 TRX 看成 −70%(实为 −18%)。
"""
import argparse, json, sys, time, datetime as dt, hashlib
from collections import defaultdict
from pathlib import Path
import warnings; warnings.filterwarnings('ignore')
from curl_cffi import requests as cr

ROOT = Path(__file__).resolve().parent.parent
ADDR_FILE = ROOT / 'tools' / 'cex_addresses.json'
BS = 'https://eth.blockscout.com/api/v2'
RPCS = ['https://ethereum-rpc.publicnode.com', 'https://eth.llamarpc.com', 'https://rpc.ankr.com/eth', 'https://cloudflare-eth.com']
PLATFORM = {  # symbol: (contract, decimals) —— Blockscout 无价或偏低,链上直读
    'KCS': ('0xf34960d9d60be18cC1D5Afc1A6F012A723a28811', 6),
    'GT':  ('0xE66747a101bFF2dBA3697199DCcE5b743b454759', 18),
    'BGB': ('0x54D2252757e1672EEaD234D27B1270728fF90581', 18),
    'LEO': ('0x2AF5D2aD76741191D15Dfe7bF6aC92d4Bd912Ca3', 18),
    'HT':  ('0x6f259637dcD74C767781E37Bc6133cd6A68aa161', 18),
}
PLATFORM_OF = {'kucoin': ['KCS'], 'gate': ['GT'], 'bitget': ['BGB'], 'bitfinex': ['LEO'], 'htx': ['HT']}
# DefiLlama 交易所储备口径不计的资产(自发/关联稳定币、自发包装币、Aave 存款凭证)—— 用于算"聚合器口径覆盖率"
LLAMA_EXCLUDE = {'USDD', 'HBTC', 'AUSDT', 'AETHUSDT', 'aEthUSDT'}
USDT_TRC20 = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'
BTCTRON = 'TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9'  # Poloniex 发行的 Tron 链 "BTC"(symbol 也叫 BTC),HTX PoR 记为 BTC-TRC20
LLAMA_SLUG = {'binance-cex': 'binance-cex', 'okx': 'okx', 'gate': 'gate', 'kucoin': 'kucoin', 'htx': 'htx', 'bitget': 'bitget', 'bitfinex': 'bitfinex', 'gemini': 'gemini', 'bitstamp': 'bitstamp', 'coinex': 'coinex', 'bybit': 'bybit', 'mexc': 'mexc', 'deribit': 'deribit', 'crypto-com': 'crypto-com', 'bingx': 'bingx'}

def log(*a):
    print(dt.datetime.utcnow().strftime('%H:%M:%S'), *a, flush=True)

def get_json(url, tries=5, base=1.0, **kw):
    """GET → json;失败返回 None。指数退避。"""
    for i in range(tries):
        try:
            r = cr.get(url, timeout=25, impersonate='chrome', **kw)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return {}
        except Exception:
            pass
        time.sleep(base * (2 ** i))
    return None

def rpc_call(to, data):
    for u in RPCS:
        try:
            j = cr.post(u, json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': to, 'data': data}, 'latest']}, timeout=20, impersonate='chrome').json()
            if 'result' in j and j['result'] not in ('0x', None):
                return int(j['result'][:66], 16)
        except Exception:
            pass
    return None

def llama_price(keys):
    j = get_json('https://coins.llama.fi/prices/current/' + ','.join(keys)) or {}
    return {k: v.get('price') for k, v in j.get('coins', {}).items()}

# ---------------- ETH ----------------
def read_eth_address(a):
    """返回 (native_usd, {sym: usd}, unpriced_count) 或 None(失败)。"""
    j = get_json(f'{BS}/addresses/{a}')
    if j is None:
        return None
    nat = 0.0
    try:
        nat = int(j.get('coin_balance') or 0) / 1e18 * float(j.get('exchange_rate') or 0)
    except Exception:
        pass
    tb = get_json(f'{BS}/addresses/{a}/token-balances')
    if tb is None:
        return None
    toks = defaultdict(float); unpriced = 0
    if isinstance(tb, list):
        for t in tb:
            tk = t.get('token') or {}
            if tk.get('type') != 'ERC-20':
                continue
            try:
                v = int(t.get('value') or 0) / 10 ** int(tk.get('decimals') or 18)
            except Exception:
                continue
            er = tk.get('exchange_rate'); sym = (tk.get('symbol') or '?')[:12]
            if er:
                toks[sym] += v * float(er)
            elif v > 0:
                unpriced += 1
    return nat, dict(toks), unpriced

def read_eth(ex, addrs, prev_failed=None, sleep=0.15):
    agg = defaultdict(float); failed = []; per = {}
    todo = prev_failed if prev_failed else addrs
    for i, a in enumerate(todo):
        r = read_eth_address(a)
        if r is None:
            failed.append(a); log(f'  {ex} ✗ {a}')
        else:
            nat, toks, unp = r
            agg['ETH'] += nat
            for s, v in toks.items():
                agg[s] += v
            per[a] = {'native_usd': nat, 'tokens_usd': sum(toks.values()), 'unpriced': unp}
        if (i + 1) % 25 == 0:
            log(f'  {ex} {i+1}/{len(todo)} cum ${sum(agg.values())/1e9:.2f}B failed {len(failed)}')
        time.sleep(sleep)
    # 平台币直读替换
    plat = {}
    for sym in PLATFORM_OF.get(ex, []):
        ca, dec = PLATFORM[sym]
        px = llama_price([f'ethereum:{ca}']).get(f'ethereum:{ca}') or 0
        units = 0.0; miss = 0
        for a in addrs:
            v = rpc_call(ca, '0x70a08231' + a[2:].lower().zfill(64))
            if v is None:
                miss += 1
            else:
                units += v / 10 ** dec
            time.sleep(0.05)
        plat[sym] = {'units': units, 'price': px, 'usd': units * px, 'miss': miss, 'blockscout_usd': agg.get(sym, 0.0)}
        agg[sym] = units * px  # 以直读替换 Blockscout 估值
    total = sum(agg.values()); excl = {k: v for k, v in agg.items() if k.upper() in {x.upper() for x in LLAMA_EXCLUDE}}
    return {'n': len(addrs), 'total_usd': total, 'total_usd_llama_caliber': total - sum(excl.values()), 'excluded_for_llama': excl, 'by_token': dict(sorted(agg.items(), key=lambda x: -x[1])), 'platform_direct': plat, 'failed': failed, 'per_address': per}

# ---------------- BTC ----------------
def read_btc(ex, addrs, sleep=0.35):
    tot = 0.0; failed = []; per = {}
    for a in addrs:
        j = get_json(f'https://mempool.space/api/address/{a}')
        if not j or 'chain_stats' not in j:
            failed.append(a); continue
        b = (j['chain_stats']['funded_txo_sum'] - j['chain_stats']['spent_txo_sum']) / 1e8
        tot += b; per[a] = b
        time.sleep(sleep)
    return {'n': len(addrs), 'btc': tot, 'failed': failed, 'per_address': per}

# ---------------- Tron ----------------
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58dec(s):
    n = 0
    for ch in s:
        n = n * 58 + B58.index(ch)
    return n.to_bytes(25, 'big')[:-4].hex()

def read_tron(ex, addrs, sleep=1.2):
    """⚠ trongrid 免费额度 3 rps:每址 2 次请求 + sleep 1.2s;getaccount 失败重试 4 次(2/4/6/8s)。"""
    av = fz = usdt = 0.0; failed = []; per = {}
    for a in addrs:
        ok = False
        for k in range(4):
            try:
                j = cr.post('https://api.trongrid.io/wallet/getaccount', json={'address': b58dec(a), 'visible': False}, timeout=20, impersonate='chrome').json()
                if 'Error' in j:
                    raise RuntimeError(j['Error'])
                bal = j.get('balance', 0) / 1e6
                # 🔴 质押四个去处都要算:frozen(V1)、frozenV2.amount(V2 自持)、delegated_frozenV2_*(质押后把资源委托给他址,TRX 仍归本址)、unfrozenV2(解押队列)
                f = (sum(x.get('frozen_balance', 0) for x in j.get('frozen', []))
                     + sum((x.get('amount') or 0) for x in j.get('frozenV2', []))
                     + (j.get('delegated_frozenV2_balance_for_bandwidth') or 0)
                     + (j.get('account_resource', {}).get('delegated_frozenV2_balance_for_energy') or 0)
                     + sum((x.get('unfreeze_amount') or 0) for x in j.get('unfrozenV2', []))) / 1e6
                ok = True; break
            except Exception:
                time.sleep(2 * (k + 1))
        if not ok:
            failed.append(a); continue
        u = None
        for u_rpc in ('https://api.trongrid.io/jsonrpc', 'https://tron-rpc.publicnode.com'):
            for _ in range(2):
                try:
                    r = cr.post(u_rpc, json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': '0x' + b58dec(USDT_TRC20)[2:], 'data': '0x70a08231' + b58dec(a)[2:].zfill(64)}, 'latest']}, timeout=20, impersonate='chrome').json()
                    if r.get('result') not in (None, '0x'):
                        u = int(r['result'], 16) / 1e6; break
                except Exception:
                    time.sleep(1.5)
            if u is not None:
                break
        if u is None:  # USDT 读失败要显式记录,不能记 0
            failed.append(a + ' (usdt)'); u = 0.0
        av += bal; fz += f; usdt += u; per[a] = {'trx_available': bal, 'trx_frozen': f, 'usdt_trc20': u}
        time.sleep(sleep)
    return {'n': len(addrs), 'trx_available': av, 'trx_frozen': fz, 'trx_total': av + fz, 'usdt_trc20': usdt, 'failed': failed, 'per_address': per}

def read_trc20(ex, addrs, contract, dec, sleep=1.2):
    """TRC20 balanceOf 直读(trongrid JSON-RPC 优先;失败显式记录)。"""
    units = 0.0; failed = []; per = {}
    for a in addrs:
        v = None
        for u_rpc in ('https://api.trongrid.io/jsonrpc', 'https://tron-rpc.publicnode.com'):
            for _ in range(2):
                try:
                    r = cr.post(u_rpc, json={'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call', 'params': [{'to': '0x' + b58dec(contract)[2:], 'data': '0x70a08231' + b58dec(a)[2:].zfill(64)}, 'latest']}, timeout=20, impersonate='chrome').json()
                    if r.get('result') not in (None, '0x'):
                        v = int(r['result'], 16) / 10 ** dec; break
                except Exception:
                    time.sleep(1.5)
            if v is not None:
                break
        if v is None:
            failed.append(a)
        else:
            units += v; per[a] = v
        time.sleep(sleep)
    return {'n': len(addrs), 'contract': contract, 'units': units, 'failed': failed, 'per_address': per}

# ---------------- DefiLlama 对照 ----------------
def llama_chain_tvls(ex):
    j = get_json(f'https://api.llama.fi/protocol/{LLAMA_SLUG.get(ex, ex)}') or {}
    ct = j.get('currentChainTvls', {})
    return {'Ethereum': ct.get('Ethereum'), 'Bitcoin': ct.get('Bitcoin'), 'Tron': ct.get('Tron'), 'total': sum(v for k, v in ct.items() if '-' not in k) if ct else None}

# ---------------- 地址刷新 ----------------
def refresh_addresses(A):
    j = get_json('https://www.binance.com/bapi/apex/v1/public/apex/market/por/address') or {}
    data = j.get('data') or []
    if data:
        A['binance-cex']['eth'] = sorted({(x.get('address') or '').lower() for x in data if (x.get('network') or '').upper() == 'ETH'})
        A['binance-cex']['btc'] = sorted({x.get('address') for x in data if (x.get('network') or '').upper() == 'BTC'})
        A['binance-cex']['tron'] = sorted({x.get('address') for x in data if (x.get('network') or '').upper() == 'TRX'})
        log('Binance PoR 地址:', {k: len(A['binance-cex'][k]) for k in ('eth', 'btc', 'tron')})
    j = get_json('https://www.binance.com/bapi/tokencanal/v2/tokencanal/lockinfo') or {}
    toks = j.get('tokens') or []
    if toks:
        A['binance-cex']['eth_lock'] = sorted({(li.get('address') or '').lower() for t in toks for li in t.get('lockInfo', []) if li.get('network') == 'ETH' and (li.get('address') or '').startswith('0x')})
        log('Binance lockinfo ETH 地址:', len(A['binance-cex']['eth_lock']))
    # ⚠ Bitstamp 接口分页(perPage ≤ 100),必须翻到底;只读第 1 页会漏掉 BTC 与大部分 ETH 地址
    # 接口每次调用的分页内容不稳定,只能翻到空页为止;按【原样地址】去重 —— 绝不能 .lower(),3… 开头的 P2SH 地址区分大小写
    allw = {}; page = 1
    while page <= 60:
        j = get_json(f'https://www.bitstamp.net/api/v2/wallet_transparency/?perPage=100&page={page}') or {}
        items = [w for v in (j.get('wallets') or {}).values() for w in v]
        if not items:
            break
        for w in items:
            allw[(w.get('address'), w.get('network'))] = w
        page += 1; time.sleep(0.4)
    allw = list(allw.values())
    if allw:
        A['bitstamp']['eth'] = sorted({w['address'].lower() for w in allw if w.get('network') == 'ethereum'})  # EVM 地址不分大小写
        A['bitstamp']['btc'] = sorted({w['address'] for w in allw if w.get('network') in ('bitcoin', 'btc')})  # 原样
        nets = {}
        for w in allw: nets[w.get('network')] = nets.get(w.get('network'), 0) + 1
        log('Bitstamp 钱包接口:', {k: len(A['bitstamp'][k]) for k in ('eth', 'btc')}, '| 页数', page - 1, '| 网络分布', nets)
    return A

def valid_btc(a):
    """比特币主网地址合法性:1…/3… 走 Base58Check(25 字节、版本 0/5、校验通过),bc1… 走 bech32 字符集与长度。
    教训:Waves 主网地址恰以 3P 开头(35 字符),仅按前缀会把别的链的地址当成 P2SH。"""
    if a.startswith('bc1'):
        return 14 <= len(a) <= 74 and all(c in '023456789acdefghjklmnpqrstuvwxyz' for c in a[3:].lower()) and a[3:] == a[3:].lower()
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    if not a or a[0] not in '13' or any(c not in alphabet for c in a): return False
    n = 0
    for c in a: n = n * 58 + alphabet.index(c)
    b = n.to_bytes(25, 'big') if n < 256 ** 25 else None
    if b is None or b[0] not in (0, 5): return False
    return hashlib.sha256(hashlib.sha256(b[:-4]).digest()).digest()[:4] == b[-4:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chain', default='eth', help='eth|btc|tron|all')
    ap.add_argument('--ex', default='', help='逗号分隔的交易所 slug,空=全部')
    ap.add_argument('--out', default='')
    ap.add_argument('--refresh-addresses', action='store_true')
    ap.add_argument('--retry-failed', default='', help='上一次输出 JSON 路径:只补读其中 failed 的地址(ETH 链)')
    args = ap.parse_args()
    A = json.load(open(ADDR_FILE, encoding='utf8'))
    if args.refresh_addresses:
        A['exchanges'] = refresh_addresses(A['exchanges'])
        A['_refreshed'] = dt.datetime.utcnow().isoformat() + 'Z'
        json.dump(A, open(ADDR_FILE, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        log('地址文件已更新', ADDR_FILE); return
    EX = A['exchanges']
    for ex, d in EX.items():  # 入清单前先做本链校验:读不到的地址第一嫌疑是"它不是这条链的"
        for k in ('btc', 'btc_por'):
            bad = [a for a in d.get(k, []) if not valid_btc(a)]
            if bad: log(f'{ex}: {k} 剔除 {len(bad)} 个非比特币地址 {bad}'); d[k] = [a for a in d[k] if valid_btc(a)]
    exs = [e for e in args.ex.split(',') if e] or list(EX)
    chains = ['eth', 'btc', 'tron'] if args.chain == 'all' else [c for c in args.chain.split(',') if c]
    prev = json.load(open(args.retry_failed)) if args.retry_failed else None
    date = dt.datetime.utcnow().strftime('%Y-%m-%d')
    out_dir = ROOT / 'data' if (ROOT / 'data').exists() else ROOT / '数据交付'
    out_path = Path(args.out) if args.out else out_dir / f'cex_reserves_{date}.json'
    res = json.load(open(out_path)) if out_path.exists() else {}
    res.setdefault('_meta', {})['generated'] = dt.datetime.utcnow().isoformat() + 'Z'
    res['_meta']['addresses_sha256'] = hashlib.sha256(open(ADDR_FILE, 'rb').read()).hexdigest()[:16]
    res['_meta']['script'] = 'tools/cex_reserves_verify.py'
    for ex in exs:
        d = EX[ex]; r = res.setdefault(ex, {})
        r['llama'] = llama_chain_tvls(ex)
        if 'eth' in chains and d.get('eth'):
            pf = (prev or {}).get(ex, {}).get('eth', {}).get('failed') if prev else None
            if prev and not pf:
                log(f'{ex}: 无失败地址可补'); 
            else:
                log(f'== {ex} ETH {len(d["eth"])} 址' + (f'(补读 {len(pf)})' if pf else ''))
                e = read_eth(ex, d['eth'], prev_failed=pf)
                if pf and 'eth' in r:  # 合并补读结果
                    old = r['eth']; old['failed'] = e['failed']
                    for a, v in e['per_address'].items():
                        old['per_address'][a] = v
                    for s, v in e['by_token'].items():
                        if s not in old.get('platform_direct', {}):
                            old['by_token'][s] = old['by_token'].get(s, 0) + v
                    old['total_usd'] = sum(old['by_token'].values()); e = old
                r['eth'] = e
                ll = r['llama']['Ethereum'] or 0
                log(f'   {ex} ETH 直读 ${e["total_usd"]/1e9:.2f}B(聚合器口径 ${e["total_usd_llama_caliber"]/1e9:.2f}B)| 聚合器 ${ll/1e9:.2f}B | 覆盖 {e["total_usd_llama_caliber"]/ll*100 if ll else 0:.0f}% | 失败 {len(e["failed"])}')
            if d.get('eth_lock'):
                r['eth_lock'] = read_eth(ex + '-lock', d['eth_lock'])
                log(f'   {ex} 锚定代币锁仓地址 ${r["eth_lock"]["total_usd"]/1e9:.2f}B')
            if d.get('eth_por'):  # 交易所【官方 PoR 清单】的 ETH 地址(与适配器清单不同时单列;对账官方页面用这一项)
                r['eth_por'] = read_eth(ex + '-por', d['eth_por'])
                log(f'   {ex} 官方 PoR 清单 ETH 地址 ${r["eth_por"]["total_usd"]/1e9:.2f}B  by_token {list(r["eth_por"]["by_token"].items())[:4]}')
        if 'btc' in chains and d.get('btc'):
            log(f'== {ex} BTC {len(d["btc"])} 址'); r['btc'] = read_btc(ex, d['btc'])
            log(f'   {ex} BTC {r["btc"]["btc"]:,.0f} 枚 失败 {len(r["btc"]["failed"])}')
        if 'btc' in chains and d.get('btc_por'):  # 官方 PoR 清单的 BTC 主网地址(对账官方页面用)
            r['btc_por'] = read_btc(ex + '-por', d['btc_por'])
            log(f'   {ex} 官方 PoR 清单 BTC {r["btc_por"]["btc"]:,.2f} 枚 失败 {len(r["btc_por"]["failed"])}')
        if 'tron' in chains and d.get('tron_por'):  # 官方 PoR 清单中的稳定币地址(USDT-TRC20 / stUSDT),与适配器的 TRX 地址集分开读
            r['tron_por'] = read_tron(ex + '-por', d['tron_por'])
            log(f'   {ex} 官方 PoR 稳定币地址 USDT-TRC20 {r["tron_por"]["usdt_trc20"]:,.0f} 失败 {len(r["tron_por"]["failed"])}')
        if 'tron' in chains and d.get('tron_btctron'):  # HTX 记作"BTC-TRC20"的 Poloniex BTCTRON(无抵押,§3e.7)
            r['tron_btctron'] = read_trc20(ex, d['tron_btctron'], BTCTRON, 8)
            log(f'   {ex} BTCTRON(BTC-TRC20)持仓 {r["tron_btctron"]["units"]:,.2f} 枚 失败 {len(r["tron_btctron"]["failed"])}')
        if 'tron' in chains and d.get('tron'):
            log(f'== {ex} Tron {len(d["tron"])} 址'); r['tron'] = read_tron(ex, d['tron'])
            log(f'   {ex} TRX 可用 {r["tron"]["trx_available"]:,.0f} + 冻结 {r["tron"]["trx_frozen"]:,.0f} | USDT-TRC20 {r["tron"]["usdt_trc20"]:,.0f} 失败 {len(r["tron"]["failed"])}')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(out_path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    log('输出', out_path)

if __name__ == '__main__':
    main()
