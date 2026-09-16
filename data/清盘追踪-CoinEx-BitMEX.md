# 清盘期储备追踪:CoinEx / BitMEX(公开储备率承诺 vs 实际链上流出)

> 观测窗口:2026-09-15 → 2026-12-22。两家交易所在同一窗口内有序清盘/关站,各自公告"资产 ≥ 负债 / 储备率 >100% / 全额兑付"。本表**逐日直读其公布地址上的链上资产**,与承诺并列,**不下偿付能力判断**(负债端外部不可验,同 REPORT.md 口径)。
>
> - **CoinEx**:2026-09-15 宣布有序清盘,提现开放至 12-22(公告 Zendesk 文章 id 53539656293908)。CET 09-29 起按 0.005 USDT 回购。
> - **BitMEX**:2026-09-23 04:00 UTC 关站(2026-07-23 宣布,bitmex.com/blog/bitmex-closure),储备见其 PoR&L 页;逾期未提收 1%/年或 $50。
>
> **地址来源**:DefiLlama-Adapters(CoinEx: projects/coinex 的 config.ethereum.owners 14 个 ETH 储备址 + helper/bitcoin-book 19 个 BTC 址 + tron 1 址;BitMEX: helper/bitcoin-book/bitmex.js 230 个 BTC 址),已并入 tools/cex_addresses.json。地址集是第三方公布的,读数是本方直读。
> **读法**:python3 tools/cex_reserves_verify.py --chain all --ex coinex,bitmex;枚数为主(不受币价影响),USD 为参照。
>
> ⚠ **一个 CoinEx 受控地址单列、不计入储备**:0x548054…(6,580 ETH + $27M USDT + $31.6M aEthUSDT)在 DefiLlama 适配器里是 getStakedEthTVL 的**信标链质押提款地址**,不是储备 owner;聚合器按"数其背后验证者质押 ETH"处理、不汇总其代币余额。本表把它**单列为质押/提款址**,不并入 CoinEx 储备(否则会把提款地址余额冒充储备)。CoinEx 储备以 14 个 owner 址为准 —— 其 ETH 侧几乎为空(≈$1.9M,与聚合器一致),储备主体是 BTC。

## 追踪表(枚数 / USD;每日 UTC 一读)

| 日期(UTC) | CoinEx 储备 BTC(枚) | CoinEx 储备 ETH 侧($,14 owner) | BitMEX BTC(枚) | Aave USDT 池现金($) / 利用率 | 单列·CoinEx 质押提款址 0x548054(ETH 枚 / USDT / aEthUSDT) | 备注 |
|---|---:|---:|---:|---:|---|---|
| 2026-09-15(基线) | 1,771($137.4M) | ≈$0(owner 代币近乎空;聚合器 ETH $1.9M 系 getStakedEthTVL 质押 TVL,非 owner 代币) | 8,183($635M) | $412.7M / 87.1% | 6,581 / $27.0M / $31.6M(≈$75M,单列不计储备) | 公告后首读;CoinEx 储备主体是 BTC,储备口径 ≈聚合器 $139.9M(近九成 BTC);BitMEX ≈$635M;两家均无明显流出 |
| 2026-09-16 | 1,521(−250,**−14.1%** 🔴X19) | ≈$0(owner 代币 $0.04M,USDT $0) | 8,173(−0.13%) | $446.2M / 85.9% | 3,981 / $21.6M / **$0**(aEthUSDT 全部赎回) | 🔴 **X19 触发**:储备 BTC 单日 −14.1%,地址集不变(19 址、0 失败)非假象;1 址下降、最大单址占 100%;最大降幅址近期出向:bc1qdllzjxky… 150.00 BTC; bc1qdllzjxky… 50.00 BTC; bc1qdllzjxky… 50.00 BTC; bc1qdllzjxky… 30.00 BTC。0x548054:aEthUSDT $31.64M 于 09-15 07:47Z 销毁=真赎回;USDT 分 3 笔共 $37M → 0x50ef5ed0(EOA,65k 笔交易热钱包形态,**与 CoinEx 已知 15 址无往来,归属未核**);1,600 ETH 经内部交易 → 0xb9391e43(EOA,27k 笔,同无关联);另约 1,000 ETH 去向未核到。owner USDT 仍 $0 ⇒ 该 $37M 未回流列出 owner。Aave 池现金反升 +$33.5M,赎回被吸收。**只记不判**:分散减少+外转,与「开放提现后用户提走」一致,但收款址归属未核,不写挤兑/外逃定性 |

## 触发/关注项

- 🔴 **CoinEx 储备 BTC 单日 −10%**(= 提现挤兑/转移)。
- 🔴 **BitMEX BTC 在 09-23 关站前后单日 −10%**。
- 🟡 **质押提款址 0x548054 的 aEthUSDT / USDT 变动**:单列观察(CoinEx 受控但非储备口径的资金池)。其 aEthUSDT $31.6M 若一次赎回仅占 Aave USDT 池现金(09-15 $412.7M)的 7.7%,当前池况可吸收。
- ⚠ **CET 回购(09-29 起 0.005 USDT)**:若用储备回购 CET,储备等额下降属正常清盘动作、非流出,单列不混入挤兑判断。

## 口径纠正记录

- 2026-09-15:首版曾把 0x548054 当作 CoinEx 储备 owner、把其 $75M 余额并入"CoinEx ETH 全资产"并据此称"聚合器漏计 40×"——**已纠正**:该址是适配器 getStakedEthTVL 的信标质押提款地址,非储备 owner;14 个真 owner 址 ETH 侧近乎空、与聚合器一致,**不存在聚合器漏计储备**。教训:对聚合器"少算"的任何断言,先核适配器源码里该地址属 owners 还是 helper 里的 staking/派生用途。

## 数据文件

- 逐日快照:data/coinex_liquidation_YYYY-MM-DD.json、data/bitmex_liquidation_YYYY-MM-DD.json。
- 基线:coinex_liquidation_2026-09-15.json、bitmex_liquidation_2026-09-15.json。
