#!/usr/bin/env python3
"""用最新 data/cex_reserves_<date>.json 与 data/por_*.json 重生成 REPORT.md / REPORT.en.md 的 §3.1–3.3 三张表(只换表格,不动读法)。用法:python3 tools/regen_tables.py data/cex_reserves_YYYY-MM-DD.json"""
import re, subprocess, sys
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
DATA=sys.argv[1] if len(sys.argv)>1 else ROOT+'data/cex_reserves_2026-09-04.json'
def tables(lang):
    out=subprocess.run(['python3',ROOT+'tools/make_tables.py',DATA,'--lang',lang],capture_output=True,text=True); 
    if out.returncode: raise SystemExit(out.stderr[-800:])
    segs=out.stdout.split('@@ETH@@'); b31=segs[0]; s2=segs[1].split('@@TRON@@'); b32=s2[0]; b33=s2[1]
    return [ '\n'.join(l for l in seg.split('\n') if l.startswith('|')) for seg in (b31,b32,b33)]
B={'zh':{'31':"- 末两列:各所官方 PoR 页面自报的 BTC(用户负债 / 交易所钱包,含托管;`tools/por_fetch.py` 抓取,Binance、Bybit 为人工登记),以及直读 ÷ 自报钱包。偏离超过 5% 标红并注明原因:差来自快照日期、地址集(适配器地址清单不是页面全部钱包)与口径(HTX 把 BTC-TRC20 与托管计入钱包),不是储备异常的判据。OKX(134,399 / 148,552,08-11)与 KuCoin(7,441 / 7,985,08-31)有自报数但未公布 BTC 地址,不在表内。Bitfinex、Gemini、Bitstamp 没有默克尔 PoR 页面,不自报逐币数;Deribit 自 2026-09-01 起停止发布 PoR(客户资产九成迁至 Coinbase 托管);Crypto.com 有页面但数字由脚本渲染,本报告尚未取快照。",
         '32':"- 末列为各所官方 PoR 自报的 ETH(用户 / 钱包,快照日各异),口径是**全链 ETH**(含 L2、质押凭证与托管),与本表以太坊主网美元读数不是同一口径,只作参照,不算差值。",
         '33':"- 末两列为各所官方 PoR 自报的 TRX 与 USDT(用户 / 钱包);USDT 是**全链合计**(ERC20 + TRC20 + 其他链),本表 USDT-TRC20 只是其中一条链,故不算差值。HTX 的 TRX 自报钱包 9,376M 与本表 18 址 9,692M(可用 + 质押)同量级;其 USDT 自报钱包 710M 中 656M 在\"ThirdParty\"(§6.2)。"},
   'en':{'31':"- The last two columns: each exchange's self-reported BTC from its official PoR page (user liabilities / exchange wallets incl. custody; fetched by `tools/por_fetch.py`, Binance and Bybit entered manually), and direct read ÷ reported wallets. Deviations over 5% are red with the reason: they come from snapshot dates, address sets (the adapter address list is not every wallet on the page) and caliber (HTX counts BTC-TRC20 and custody as wallets), and are not a reserve-anomaly criterion. OKX (134,399 / 148,552, 08-11) and KuCoin (7,441 / 7,985, 08-31) self-report BTC but publish no BTC addresses, so they are not in the table. Bitfinex, Gemini and Bitstamp have no Merkle PoR page and report no per-coin figures; Deribit stopped publishing PoR on 2026-09-01 (90% of client assets moved to Coinbase custody); Crypto.com has a page but its figures are script-rendered and no snapshot has been taken yet.",
         '32':"- The last column is each exchange's self-reported ETH (users / wallets, snapshot dates vary). Its caliber is **ETH across all chains** (L2s, staking receipts and custody included), not the same as this table's Ethereum-mainnet dollar read, so it is shown for reference only and no difference is computed.",
         '33':"- The last two columns are each exchange's self-reported TRX and USDT (users / wallets); USDT is the **all-chain total** (ERC20 + TRC20 + others) while this table's USDT-TRC20 is one chain, so no difference is computed. HTX's reported TRX wallets of 9,376M are in the same range as this table's 9,692M across 18 addresses (available + staked); of its reported 710M USDT wallets, 656M sit in \"ThirdParty\" (§6.2)."}}
for f,lang,rh in (('REPORT.md','zh','**读法**'),('REPORT.en.md','en','**How to read**')):
    s=open(ROOT+f,encoding='utf-8').read(); t31,t32,t33=tables(lang)
    for head,tab in (('### 3.1',t31),('### 3.2',t32),('### 3.3',t33)):
        a=s.index(head); ts=s.index('\n|',a)+1; te=s.index('\n\n',ts); s=s[:ts]+tab+s[te:]
    open(ROOT+f,'w',encoding='utf-8').write(s); print(f,'tables ok'); continue
    a=s.index('### 3.1'); c=s.index('### 3.2',a); seg=s[a:c]
    seg=re.sub(r"\n- (末列为各所官方 PoR 页面自报的 BTC|The last column is each exchange's self-reported BTC)[^\n]*",'',seg)
    seg=seg.rstrip('\n')+'\n'+B[lang]['31']+'\n\n'; s=s[:a]+seg+s[c:]
    for head,nxt,key in (('### 3.2','### 3.3','32'),('### 3.3','## 4.','33')):
        a=s.index(head); c=s.index(nxt,a); seg=s[a:c]
        if B[lang][key][:25] not in seg: seg=seg.rstrip('\n')+'\n'+B[lang][key]+'\n\n'; s=s[:a]+seg+s[c:]
    open(ROOT+f,'w',encoding='utf-8').write(s); print(f,'ok')
