#!/usr/bin/env python3
"""生成报告 §2「全景:链上储备前 20 名」表(DefiLlama 公开地址口径)。
口径:①样本 = DefiLlama CEX 榜链上资产前 20 名,不做主观增删;②BTC/ETH/稳定币/关联币按各所代币构成分类;
     ③关联币 = 交易所或其控制人发行的资产(AFFIL 表);④1 年净流量 = 储备变动剔币价效应后的残差(价格基准见 PRICE_CHG)。
用法:python3 tools/panorama.py [--lang zh|en] [--out -]
"""
import json, sys, time, datetime, warnings
warnings.filterwarnings('ignore')
from curl_cffi import requests as cr
LANG = 'en' if '--lang' in sys.argv and sys.argv[sys.argv.index('--lang') + 1] == 'en' else 'zh'
UA = dict(timeout=180, impersonate='chrome')
def get(u):
    for i in range(5):
        r = cr.get(u, **UA)
        if r.status_code == 200: return r.json()
        time.sleep(10)
    raise SystemExit(f'读取失败 {u}')
STABLE = {'USDT','USDC','FDUSD','DAI','TUSD','BUSD','USDE','PYUSD','USD1','USDS','SUSDS','GUSD','USDP','FRAX','LUSD','USDG','RLUSD','EURC','EURCV','AUSDT','AETHUSDT','AUSDC','AETHUSDC','SUSDE','USDTB','USDY','USDC.E','USDT.E','EURT','XAUT'}
BTC_T = {'BTC','WBTC','BTCB','CBBTC','TBTC','FBTC','LBTC','SOLVBTC','BTC.B'}
ETH_T = {'ETH','WETH','STETH','WSTETH','WBETH','RETH','CBETH','BETH','WEETH','METH','EZETH','RSETH','AETHWETH'}
# 关联币:交易所或其控制人发行(与 §4.3 分类同源;USDD/HBTC/BTCTRON 属自发/关联资产,聚合器口径本就不计)
AFFIL = {'binance':{'BNB'},'okx':{'OKB'},'bitfinex':{'LEO'},'bybit':{'MNT'},'gate':{'GT'},'bitget':{'BGB'},
         'mexc':{'MX'},'htx':{'TRX','HT','HTX','TRON'},'kucoin':{'KCS'},'crypto.com':{'CRO'},'swissborg':{'BORG'},
         'poloniex':{'TRX','SUN','JST','USDD','WIN','BTT','NFT'},'bitkub':{'KUB'},'hashkey':{'HSK'},'gemini':{'GUSD'},'korbit':set(),'phemex':set(),'probit global':set()}   # 按【所名小写】映射:榜单 slug 与 protocol slug 可能不一致
PRICE_CHG = {'BTC':-0.280,'ETH':-0.429,'STABLE':0.0,'OTHER':-0.40}   # 一年币价基准(币安日线),用于剔价
def aff_str(a): return ','.join(sorted(a)) if a else '—'
def cls(sym, aff):
    s = (sym or '').upper()
    if s in aff: return 'AFFIL'
    if s in BTC_T: return 'BTC'
    if s in ETH_T: return 'ETH'
    if s in STABLE: return 'STABLE'
    return 'OTHER'
board = get('https://api.llama.fi/cexs')
cexs = board['cexs'] if isinstance(board, dict) and 'cexs' in board else board
rows = []
for c in sorted(cexs, key=lambda x: -(x.get('currentTvl') or 0))[:20]:   # ⚠ 榜单条目的 'tvl' 字段恒为 0,真值在 currentTvl —— 用错会得到接口原始顺序而非排名
    slug = c.get('slug') or c.get('gecko_id') or c['name'].lower()
    rows.append(dict(name=c['name'], slug=slug, tvl=c.get('currentTvl') or 0, cg=c.get('cgId'), raw=c))
print(f'榜单前 20(读取 {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC):', [r['name'] for r in rows], flush=True)
out = []
for r in rows:
    slug = r['slug']; aff = AFFIL.get(r['name'].lower(), AFFIL.get(slug, set()))
    try: p = get(f'https://api.llama.fi/protocol/{slug}')
    except SystemExit: print(f'  {r["name"]} 读取失败,跳过'); continue
    # 当前代币构成(所有链合计)
    agg = {}
    for chain, ct in (p.get('chainTvls') or {}).items():
        if '-' in chain or chain in ('staking','borrowed','pool2','vesting'): continue
        tu = ct.get('tokensInUsd') or []
        if not tu: continue
        for sym, v in (tu[-1].get('tokens') or {}).items(): agg[cls(sym, aff)] = agg.get(cls(sym, aff), 0) + float(v or 0)
    tot = sum(agg.values()) or r['tvl'] or 1
    # 校验:逐币加总须与 tvl 序列一致(不一致说明链键口径有重复,弃用该行的构成)
    tvl_now = (p.get('tvl') or [{}])[-1].get('totalLiquidityUSD') or 0
    comp_ok = tvl_now > 0 and abs(tot / tvl_now - 1) < 0.02
    # 1 年变动(tvl 序列)与价格基准(按构成加权),超额 = 变动 − 基准(减法,与 §2 原口径一致)
    tv = p.get('tvl') or []
    tgt = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    prev = [x for x in tv if time.strftime('%Y-%m-%d', time.gmtime(x['date'])) <= tgt]
    chg = base = flow = None; win_days = 365; win_from = tgt
    if not prev and tv:   # 序列不足一年:用序列起点并【标出实际窗口】(极值/变动类结论必须附窗口起止)
        prev = [tv[0]]; win_from = time.strftime('%Y-%m-%d', time.gmtime(tv[0]['date']))
        win_days = (datetime.date.today() - datetime.date.fromisoformat(win_from)).days
    if prev and tvl_now:
        a = prev[-1]['totalLiquidityUSD']
        if a > 0:
            chg = tvl_now / a - 1
            base = sum(agg.get(k, 0) / tot * PRICE_CHG[k if k in PRICE_CHG else 'OTHER'] for k in agg) * (win_days / 365)
            flow = chg - base
    out.append(dict(name=r['name'], slug=slug, tvl=tvl_now or tot, comp_ok=comp_ok, pct={k: agg.get(k, 0) / tot for k in ('BTC','ETH','STABLE','AFFIL')},
                    chg_1y=chg, price_base=base, flow=flow, window_from=win_from, window_days=win_days, aff_sym=','.join(sorted(aff)) if aff else '—'))
    print(f"  {r['name']:13s} ${(tvl_now or tot)/1e9:7.1f}B BTC {agg.get('BTC',0)/tot:4.0%} ETH {agg.get('ETH',0)/tot:4.0%} 稳 {agg.get('STABLE',0)/tot:4.0%} 关联 {agg.get('AFFIL',0)/tot:4.0%}({aff_str(aff)}) | 1y变动 {('%+.1f%%'%(chg*100)) if chg is not None else '—':>8s} 基准 {('%+.1f%%'%(base*100)) if base is not None else '—':>7s} 超额 {('%+.1f%%'%(flow*100)) if flow is not None else '—':>8s} {'' if win_days>=365 else '⚠窗口仅 %d 天(起 %s)'%(win_days,win_from)}{'' if comp_ok else ' ⚠构成与tvl不符'}", flush=True)
    time.sleep(1)
json.dump(dict(read_at=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), rows=out),
          open('data/panorama_%s.json' % datetime.date.today(), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('写入 data/panorama_%s.json' % datetime.date.today())
