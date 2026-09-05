# CEX Reserves · 交易所储备核查 / Top Exchange Reserves Check

> **Read the chain, not the press release.** / **读链,不读公告。**

**🔎 Online / 在线页面:** 中文 <https://ronfi.github.io/cex-reserves/> · English <https://ronfi.github.io/cex-reserves/en/>

---

## 中文

本仓库公开维护一份**头部加密交易所储备核查报告**,以及**可复现它每一个数字的脚本与地址清单**。

- 报告只使用三类可核验数据:**链上直读**(BTC / ETH / Tron 公共节点与浏览器 API)、**交易所官方储备证明(PoR)页面与地址清单**、**公开聚合器(DefiLlama)**。媒体报道只作线索,标 ⚠,不进入任何表格。
- 每一张表都能用仓库脚本重新生成;地址清单在 `tools/cex_addresses.json`,本版输出在 `data/`。
- 报告对每家交易所用同一套读法;凡本方认定的异常,不论哪家,都用红色标出并附核验方法。
- 每周一 00:00 UTC 更新。

### 复现

```bash
pip install curl_cffi
python3 tools/cex_reserves_verify.py --chain all            # 三链全量(约 40 分钟,受公共节点限速)
python3 tools/cex_reserves_verify.py --chain eth --ex htx   # 只读一家
python3 tools/cex_reserves_verify.py --refresh-addresses    # 重拉 Binance PoR / lockinfo 与 Bitstamp 钱包清单
python3 tools/por_fetch.py                                  # 各所官方 PoR 自报数(OKX/Bitget/KuCoin/Gate/MEXC 接口,HTX GitHub CSV)→ data/por_<date>.json
python3 tools/regen_tables.py data/cex_reserves_<date>.json # 重生成中英两稿的 §3.1–3.3 三表
python3 tools/por_trx_delta.py --since 2026-08-01           # Poloniex TRX 地址逐址:快照 vs 链上(报告 §7.1)
python3 tools/beacon_validators.py <提款地址…>               # 按提款地址数信标链验证者与余额(报告 §3.2)
python3 tools/build_site.py --archive                       # 生成中英页面并把本期存入 docs/archive/(不带 --archive 只重建不存档)
```

### 免责声明

一切内容均为公开数据的整理与核对,**不构成投资建议**,不构成对任何机构偿付能力的断言。交易所负债端(用户资产)只有交易所自己知道;本报告能核的是"公布的地址上有没有那些币"。

---

## English

This repository maintains a public **reserves check of the top crypto exchanges**, together with **the scripts and address lists that reproduce every number in it**.

- The report uses only three kinds of verifiable data: **direct on-chain reads** (BTC / ETH / Tron public nodes and explorer APIs), **each exchange's official proof-of-reserves (PoR) page and address list**, and **the public aggregator DefiLlama**. Media reports are used only as leads, marked ⚠, and never enter a table.
- Every table can be regenerated with the scripts here; address lists are in `tools/cex_addresses.json`, this edition's output in `data/`.
- Every exchange is read the same way; whatever this report identifies as an anomaly is marked red, with its verification method, regardless of which exchange it is.
- Updated every Monday 00:00 UTC.

### Reproduce

```bash
pip install curl_cffi
python3 tools/cex_reserves_verify.py --chain all            # all three chains (~40 min, public-node rate limits)
python3 tools/cex_reserves_verify.py --chain eth --ex htx   # one exchange only
python3 tools/cex_reserves_verify.py --refresh-addresses    # re-pull Binance PoR / lockinfo and Bitstamp wallet lists
python3 tools/por_fetch.py                                  # official PoR self-reported figures (OKX/Bitget/KuCoin/Gate/MEXC APIs, HTX GitHub CSV) → data/por_<date>.json
python3 tools/regen_tables.py data/cex_reserves_<date>.json # regenerate §3.1–3.3 tables in both language editions
python3 tools/por_trx_delta.py --since 2026-08-01           # Poloniex TRX addresses one by one: snapshot vs chain (report §7.1)
python3 tools/beacon_validators.py <withdrawal addresses…>  # Beacon-chain validators and balances by withdrawal address (report §3.2)
python3 tools/build_site.py --archive                       # build both pages and archive this edition under docs/archive/ (omit --archive to rebuild without archiving)
```

### Disclaimer

Everything here is a compilation and cross-check of public data. It is **not investment advice** and makes no claim about any institution's solvency. Only an exchange knows its liability side (user assets); what this report can verify is whether the coins are on the published addresses.

---

## 打赏 / Support

如果这些核对帮您省下了自己动手核一遍的时间,欢迎支持本项目持续维护;地址只以 main 分支的 [DONATE.md](DONATE.md) 为准,其他地方看到的地址请勿使用。
If these checks saved you the work of verifying it yourself, support for the project's continued maintenance is welcome; use only the addresses in [DONATE.md](DONATE.md) on the main branch, and no address seen anywhere else.

## License

报告内容 / report content **CC BY-NC-ND 4.0**;脚本 / scripts **MIT**。详见 / see [LICENSE](LICENSE).
