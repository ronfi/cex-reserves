# 头部交易所储备核查 · 2026-09

> 各表标题另有各自的读取时间。全部数字可用本仓库 `tools/cex_reserves_verify.py` 重新读取;输出快照在 `data/cex_reserves_2026-09-04.json`。
> 口径纪律:**链上直读 > 官方 PoR 页面 > 公开聚合器 > 媒体**。前三类进表;媒体只作线索,标 ⚠,不进表。
> 本页不对任何交易所的偿付能力作判断,只呈现可核验的事实,以及各来源之间的差异。

## 0. 摘要

1. 头部交易所里,**同时具备四类关联资产的只有 HTX**:平台币(HTX 币)、关联稳定币(USDD)、自发包装币(BTC-TRC20、HBTC)、JustLend 生息凭证(stUSDT/jUSDD)。其余各所最多一种(分类与 FTX 三条判据见 §4)。
2. **HTX 自报储备率"均超 100%",但按链上可核口径:USDT 自有钱包只覆盖负债的 5.8%,BTC 41%,ETH 25.5%;总储备的 19.1% 在不披露身份的"第三方托管",47% 是 TRX 且其中 69% 处于质押。**
3. Binance / OKX 的储备在 BTC 与 ETH 链上可 99–103% 对上;Bitfinex、Gate、KuCoin、Gemini 亦在 95–101%。各所均自报储备率 >100%;本报告只能核验其中可在链上读到的部分,各所可核比例见 §3。

## 1. 方法:三层数据,只信最底层

| 层 | 是什么 | 本报告用法 |
|---|---|---|
| 链上直读 | 拿交易所公布的地址,直接读 BTC(mempool.space)、ETH 全部有报价 ERC20(Blockscout)、Tron(trongrid `getaccount`,含质押) | **主判据**;每地址失败记录在输出 JSON |
| 官方 PoR 页 | 各所储备证明页面(负债、自报储备、托管栏) | 负债端唯一来源;**本报告不能验证负债总额** |
| 聚合器(DefiLlama) | 按其自维护地址集汇总。下文 "DefiLlama-Adapters" 指其开源仓库里每家交易所的抓取脚本与地址清单(<https://github.com/DefiLlama/DefiLlama-Adapters/tree/main/projects>) | 全景对比;两条口径规则见下 |

**聚合器口径规则**

1. 计平台币,不计交易所自发或关联的稳定币(USDD)、自发包装币(HBTC / BTCTRON)、Aave 存款凭证。
2. Binance 行含其为 BSC 锚定代币锁定的抵押储备($12.3B),不是用户资产。
3. 地址集可与官方 PoR 清单不同(HTX:DefiLlama-Adapters 57 址 vs 官方 11 址)。

## 2. 全景:链上储备前 20 名(DefiLlama 公开地址口径,读取于 2026-09-04 22:30 UTC)

样本规则:**DefiLlama CEX 榜链上资产前 20 名**,不做主观增删;Coinbase / Kraken / Upbit 不公布地址,不在榜内。

- 自查入口:榜单页 <https://defillama.com/cexs>;单所页 `https://defillama.com/cex/<slug>`(如 <https://defillama.com/cex/htx>、<https://defillama.com/cex/binance-cex>);数据接口 `https://api.llama.fi/protocol/<slug>`(含各链 `currentChainTvls` 与代币构成);各所DefiLlama-Adapters源码 <https://github.com/DefiLlama/DefiLlama-Adapters/tree/main/projects>(地址清单或抓取逻辑在此)。

- "关联币"= 交易所或其控制人发行的资产;红标规则统一为 **关联币占储备 >30%**。
- "1 年净流量"= 储备变动剔除币价效应后的残差(正 = 净流入);币价基准按币安日线:BTC -28.0%、ETH -42.9%、稳定币 0、关联币/其他 −40% 近似。
- ⚠ Bitstamp 行为聚合器 09-04 22:30 UTC 读数;本报告直读 39,951 BTC(§3.1)。

| # | 所 | 链上储备 | BTC | ETH | 稳定币 | 关联币 | 1 年净流量 |
|---|---|---|---|---|---|---|---|
| 1 | Binance | $167.6B | 31% | 11% | 32% | 15%(BNB) | +13.4% |
| 2 | OKX | $30.0B | 38% | 10% | 38% | 4%(OKB) | +28.6% |
| 3 | Bitfinex | $19.1B | 61% | 3% | 2% | <mark class="r">**32%(LEO)**</mark> | +2.3% |
| 4 | Bybit | $16.0B | 29% | 10% | 36% | 4%(MNT) | -9.7% |
| 5 | Robinhood(经纪商) | $14.5B | 77% | 21% | 0% | 0% | -1.0% |
| 6 | Gate | $6.8B | 22% | 16% | 16% | 14%(GT) | +12.3% |
| 7 | Bitget | $6.0B | 40% | 7% | 18% | 8%(BGB) | +33.6% |
| 8 | Gemini | $5.3B | 85% | 13% | 0% | 0% | -14.9% |
| 9 | MEXC | $5.3B | 18% | 3% | 45% | 11%(MX) | +51.1% |
| 10 | Deribit | $5.1B | 77% | 11% | 11% | 0% | +28.4% |
| 11 | Bitstamp | $4.7B | 69% | 21% | 1% | 0% | +121.3% ⚠ 非资金流入(见读法) |
| 12 | HTX | $3.7B | 18% | 2% | 0% | <mark class="r">**77%(TRX + HT)**</mark> | -10.1% |
| 13 | KuCoin | $3.2B | 20% | 9% | 30% | 16%(KCS) | -12.1% |
| 14 | Crypto.com | $2.5B | 74% | 7% | 9% | 1%(CRO) | -7.1% |
| 15 | HashKey | $1.7B | 65% | 25% | 5% | 0% | +30.8% |
| 16 | Poloniex | $1.5B | 49% | 39% | 1% | 2%(关联体系代币) | +61.1% ⚠ 非客户流入(见读法与 §7) |
| 17 | Bitkub | $1.4B | 65% | 14% | 3% | 0% | +33.6% |
| 18 | SwissBorg | $1.0B | 43% | 14% | 6% | 15%(BORG) | -2.5% |
| 19 | BitMEX | $0.8B | 87% | 0% | 13% | 0% | -60.5%(2026-09-23 自愿关停,清退前提币) |
| 20 | OSL | $0.7B | 75% | 19% | 3% | 0% | +16.1% |

**读法**

- 关联币占储备超过三成的只有两家:**HTX 77%、Bitfinex 32%**。LEO 是 iFinex 2019 年发行的平台币(非稳定币,靠营收回购销毁支撑),与 BNB、OKB、GT、KCS 同类,按同一规则标注。
- Bitfinex 其余 61% 是 BTC。
- Bitstamp +121.3% 不是资金流入:聚合器DefiLlama-Adapters的分页缺陷修复后地址集补全(DefiLlama-Adapters PR #20878,09-04 合并),其 BTC 读数由 4,180 变为 40,167。
- Poloniex +61.1% 不是客户流入:2026-05-30 至 06-04,71,993 stETH、806M sUSDS、1,723 WBTC 经两个 Poloniex 公布地址转入 Poloniex 9(一址占其储备 63%)。stETH 这一路往上可追到 HTX 地址 `0x18709E89…`(归属核实见 §7);WBTC 1,723 与其中 200M sUSDS 同样追到该地址;另 606M sUSDS 来自一个自行铸造 sUSDS 的未标注枢纽地址,HTX 来源未能在链上确立。逐跳见 §7。
- HTX 其余是 18% BTC(其中一半是 §7.2 的 BTC-TRC20)与 2% ETH;聚合器地址集上没有稳定币。稳定币为 0 的还有 Gemini、Bitstamp、Robinhood,本身不构成差异项;HTX 官方 PoR 清单自有 USDT 的读数见 §6.2。

## 3. 公布地址链上直读对账(本报告主判据)

§2 是聚合器口径;本节是**本报告自己读链**:拿各所公布的地址(官方 PoR 清单或DefiLlama-Adapters源码,见 `tools/cex_addresses.json`),逐地址读 BTC / ETH 全资产 / Tron,再与聚合器对账。**表由 `tools/make_tables.py` 从 `data/cex_reserves_2026-09-04.json` 生成**,每个地址的读数与失败记录都在该文件里。

### 3.1 BTC 链(mempool.space 直读 vs 聚合器;差值 ≤1% 绿、>5% 红)

| 所 | 公布地址(读到/总) | 直读 BTC | 聚合器 BTC(≈) | 差 | PoR 自报 BTC:用户 / 钱包(快照日) | 直读 − 自报钱包 |
|---|---|---|---|---|---|---|
| Binance | 61/61 | 640,647 | 640,647 | <span class="ok">+0.0%</span> | 656,644 / 658,293(08-01) | -2.7% |
| Bitfinex | 3/3 | 146,853 | 146,973 | <span class="ok">-0.1%</span> | — | — |
| Bybit | 25/25 | 58,141 | 58,192 | <span class="ok">-0.1%</span> | 56,438 / 59,064(07-23) | -1.6% |
| Gate | 13/13 | 18,704 | 19,040 | -1.8% | 22,436 / 27,550(08-19) | <mark class="r">-32.1%</mark>(DefiLlama-Adapters清单 13 址不是页面全部钱包(Gate 未公布 BTC 地址)) |
| Bitget | 19/19 | 29,579 | 29,540 | <span class="ok">+0.1%</span> | 26,811 / 35,837(08-20) | <mark class="r">-17.5%</mark>(适配器 19 址不是页面全部钱包;页面钱包含 BSC/Lightning 等链 535 枚) |
| MEXC | 34/34 | 11,732 | 11,741 | <span class="ok">-0.1%</span> | 4,282 / 12,313(08-09) | -4.7% |
| Gemini | 4/4 | 56,351 | 56,396 | <span class="ok">-0.1%</span> | — | — |
| Deribit | 17/17 | 49,431 | 49,326 | <span class="ok">+0.2%</span> | — | — |
| HTX | 11/11 | 8,376 | 8,280 | +1.2% | 19,933 / 20,472(08-01) | <mark class="r">-59.1%</mark>(自报钱包含 BTC-TRC20 10,399 + 托管 1,689 + BTC-SOL/jWBTC 175;原生 8,209 vs 直读 +2%) |
| Crypto.com | 8/8 | 22,722 | 22,739 | <span class="ok">-0.1%</span> | — | — |
| Bitstamp | 507/507 | 39,951 | 41,125 | -2.9% | — | — |

**读法**

- **十一所全部对上**(差 ≤1.2%),聚合器的 BTC 数可直接引用。
- HTX 的行是DefiLlama-Adapters清单 11 址;其官方 PoR 清单为 7 址,链上 8,072 枚(§6.2)。
- Gate 清单里曾混入 3 个以 `3P` 开头的字符串,两个 BTC 浏览器均 404;解码后它们不是比特币地址(35 字符、校验失败),而是 DefiLlama-Adapters `waves` 段里的 Waves 链地址(Waves 主网地址恰以 3P 开头),本报告抽取时按前缀误归为 BTC。已剔除,并在脚本里加入地址合法性校验。
- 末两列:各所官方 PoR 页面自报的 BTC(用户负债 / 交易所钱包,含托管;`tools/por_fetch.py` 抓取,Binance、Bybit 为人工登记),以及直读相对自报钱包的差额(百分比)。差额超过 5% 标红并注明原因:差来自快照日期、地址集(DefiLlama-Adapters地址清单不是页面全部钱包)与口径(HTX 把 BTC-TRC20 与托管计入钱包),不作为储备核查的判据。OKX(134,399 / 148,552,08-11)与 KuCoin(7,441 / 7,985,08-31)有自报数但未公布 BTC 地址,不在表内。Bitfinex、Gemini、Bitstamp 没有默克尔 PoR 页面,不自报逐币数;Deribit 自 2026-09-01 起停止发布 PoR(客户资产九成迁至 Coinbase 托管);Crypto.com 有页面但数字由脚本渲染,本报告尚未取快照。

### 3.2 ETH 链(Blockscout 全资产直读 vs 聚合器;"聚合器口径"列剔 USDD/HBTC/aEthUSDT;覆盖 95–105% 绿、<90% 或 >110% 红)

| 所 | 地址数 | 全资产直读 | 聚合器口径直读 | 聚合器 | 覆盖 | 失败地址 | PoR 自报 ETH:用户 / 钱包(快照日) |
|---|---|---|---|---|---|---|---|
| Binance | 37 + 锁仓 2 | $68.70B | $68.69B | $69.16B | <span class="ok">99%</span> | 0 | ? / 3,991,221(08-01) |
| OKX | 323 | $12.90B | $12.90B | $13.52B | <span class="ok">95%</span> | 0 | 1,725,703 / 1,749,426(Aug 2026) |
| Bitfinex | 9 | $7.15B | $7.15B | $7.06B | <span class="ok">101%</span> | 0 | — |
| Gate | 91 | $3.03B | $3.03B | $3.01B | <span class="ok">101%</span> | 0 | 375,430 / 458,203(08-19) |
| Bitget | 80 | $1.59B | $1.59B | $1.65B | <span class="ok">96%</span> | 0 | 123,688 / 190,090(08-20) |
| Gemini | 5 | $0.78B | $0.78B | $0.79B | <span class="ok">98%</span> | 0 | — |
| HTX | 57 | $0.22B | $0.13B | $0.12B | 108% | 0 | 122,077 / 122,627(08-01) |
| KuCoin | 96 | $1.59B | $1.59B | $1.60B | <span class="ok">99%</span> | 0 | 101,664 / 118,497(08-31) |
| Bitstamp | 64 | $0.59B | $0.59B | $1.15B | <mark class="n">51%*</mark> | 0 | — |

**读法**

- **八所 95–101%**,聚合器可引用。
- HTX 全资产直读 $0.22B 高于聚合器 $0.12B,差额恰为 USDD $45M + HBTC $42M;聚合器不计交易所自发或关联资产(§1 规则),同口径后为 108%。
- \* Bitstamp 51%:口径差,不是地址差。DefiLlama 把以 Bitstamp 提款地址为凭证的信标链质押 ETH(≈23.3 万,验证者 8,011 个)全部计入 Bitstamp 储备;本报告不计,原因是质押 ETH 不在任何公布地址的余额上,且四个提款地址里两个不在 Bitstamp 公布的清单内,归属依据只有聚合器自己的地址表。加回这部分后两边对上。独立核法见 `tools/beacon_validators.py`(§9)。
- Binance 行含锚定代币锁仓 2 址($12.3B),不是用户资产。"锚定代币锁仓"指 Binance 为其在 BNB Chain 上发行的 Binance-Peg 代币(BSC 版 USDT、USDC、ETH 等)在以太坊主网锁定的原生抵押品,负债方是这些锚定币的持有人,而非交易所客户;地址来自 Binance 的 lockinfo 端点,不在其 PoR 清单内;已向聚合器提出拆分提案(DefiLlama-Adapters PR #20885,待维护者处理)。
- "失败地址"全部为 0(OKX 一址补读后清零)。
- 末列为各所官方 PoR 自报的 ETH(用户 / 钱包,快照日各异),口径是**全链 ETH**(含 L2、质押凭证与托管),与本表以太坊主网美元读数不是同一口径,只作参照,不算差值。

### 3.3 Tron 链(trongrid `getaccount` 含四项质押 + USDT-TRC20 直读)

| 所 | 地址数 | TRX 可用 | TRX 质押中 | USDT-TRC20 | PoR 自报 TRX:用户 / 钱包 | PoR 自报 USDT(全链):用户 / 钱包 |
|---|---|---|---|---|---|---|
| Binance | 25 | 2,287M | 0M | 897.1M | — | — |
| OKX | 23 | 107M | 0M | 273.2M | — | 8,118M / 8,637M(Aug 2026) |
| Bitfinex | 2 | 28M | 0M | 76.8M | — | — |
| Gate | 11 | 15M | 0M | 63.7M | 58M / 179M(08-19) | 660M / 721M(08-19) |
| Bitget | 29 | 5M | 0M | 254.1M | — | 1,454M / 1,456M(08-20) |
| HTX | 18 | 3,046M | 6,646M | 0.0M | ? / 9,376M(08-01) | 926M / 710M(08-01) |
| KuCoin | 24 | 14M | 0M | 148.7M | — | 955M / 1,059M(08-31) |

**读法**

- **聚合器不可引用。** 它漏计 USDT-TRC20(Bitget 公布地址持 242M,聚合器记 0),其 `eth_getBalance` 读法也不含质押中的 TRX。
- Tron 的"冻结"(freeze)是其官方术语,指把 TRX 质押给网络换取带宽、能量与投票权:所有权不变、可随时发起解押、解押后 14 天到账;它不是借贷抵押,也不是被平台或司法冻结。本报告统一写"质押"。质押有四个去处:V1 质押、V2 自持质押、**委托给他址的质押**(TRX 仍归本址)、解押队列;表中"质押中"四项全计。OKX 的 5.2 亿、Poloniex 的 2,400 万都是委托质押,只读 `balance + frozenV2` 会看不到(§7.1)。
- HTX 表中 18 个 Tron 地址是DefiLlama-Adapters清单里的 TRX 冷钱包,上面没有 USDT 属正常;**HTX 官方 PoR 的 USDT-TRC20 另有 5 个地址**:08-01 快照 13.24M,09-04 链上 <mark class="r">1.91M</mark>(低于用户 USDT 负债的 1%,§10 规则;`TK86…` 的 11.33M 已转空);USDT-ERC20 1 址 1.05M → 0。用户 USDT 负债 926M 的其余部分在"ThirdParty"(§6.2)。
- 末两列为各所官方 PoR 自报的 TRX 与 USDT(用户 / 钱包);USDT 是**全链合计**(ERC20 + TRC20 + 其他链),本表 USDT-TRC20 只是其中一条链,故不算差值。HTX 的 TRX 自报钱包 9,376M 与本表 18 址 9,692M(可用 + 质押)同量级;其 USDT 自报钱包 710M 中 656M 在"ThirdParty"(§6.2)。

## 4. 关联币占储备的比重:FTX 的三项结构性前提与各所对照

### 4.1 FTX 的结构性前提是什么(⚠ 公开报道级,仅作判据来源)

FTX 2022-11 倒闭前的资产负债结构是本章判据的来源。要点三条:

- **自家币是资产主体**:CoinDesk 2022-11-02 披露 FTX 关联做市商 Alameda 的资产负债表,资产 $146 亿中 $36.6 亿是 FTX 平台币 FTT,另有 $21.6 亿 "FTT 抵押品",FTT 相关项超过资产的三分之一(<https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet>)。
- **自家币没有盘口**:FTT 流通盘大部分在 FTX 与 Alameda 自己手里,市值是挂牌价乘以数量,不是能卖出的钱;11-06 Binance 宣布出售所持 FTT,随后三天 FTT 跌去八成。
- **负债端不透明**:客户存款被挪给 Alameda 使用,外界看不到负债与资产的真实对应;11-08 暂停提币,11-11 申请破产。

判据:**致命的不是"持有自家币",是三条同时成立** —— ①自家币是储备主体;②自家币无盘口;③负债端不透明。下面按同一套规则逐所对照。

### 4.2 按所:关联币占储备(数据同 §2;红标规则与 §2 相同:关联币占储备 >30%)

"硬资产"= BTC + ETH + 稳定币;两者之和不足 100% 的余量是其他币(SOL、XRP 等)。

| 所 | 关联币 | 占储备 | 硬资产 |
|---|---|---|---|
| HTX | TRX + HTX 币 | <mark class="r">**77%**</mark> | 20% |
| Bitfinex | LEO | <mark class="r">**32%**</mark> | 66% |
| KuCoin | KCS | 16% | 59% |
| SwissBorg | BORG | 15% | 63% |
| Binance | BNB | 15% | 74% |
| Gate | GT | 14% | 54% |
| MEXC | MX | 11% | 66% |
| Bitget | BGB | 8% | 65% |
| OKX | OKB | 4% | 86% |
| Bybit | MNT | 4% | 75% |
| Poloniex | 关联体系代币 | 2% | 89% |
| Crypto.com | CRO | 1% | 90% |
| Robinhood、Gemini、Deribit、Bitstamp、HashKey、Bitkub、BitMEX、OSL | — | 0% | 77–100% |

- 超过三成的两家:HTX 77%、Bitfinex 32%。两家的差别在硬资产:Bitfinex 硬资产 66%,是 LEO 的两倍;HTX 硬资产 20%,关联币是它的近四倍。关联币是否超过硬资产,是 §4.4 判据 ① 的口径。
- 上表是聚合器口径(只认交易所公布的地址,且剔除自发/关联资产)。按 HTX 官方 PoR 快照的自报口径(§5、§6.2):TRX 占 47%、HTX 币 5.7%,另 BTC 行的 51% 是 Poloniex 发行的 BTC-TRC20(§7)。

### 4.3 关联资产按性质分四类

上表按"所"排;下面按"东西"排,一类一块。同一家所的关联资产可以横跨四类。

**① 平台币**

| 项 | 内容 |
|---|---|
| 资产 | BNB、LEO、OKB、GT、KCS、BGB、MX、MNT、CRO、BORG、HTX 币 |
| 发行方 / 机制 | 交易所自发,价值 = 交易所自身信用 |
| 规模与持有(一手) | LEO $6.3B 在 Bitfinex 储备;HTX 币 HTX 自持供给 23%,仅本所有成交(§6.2、§8) |
| 可核性 | 余额可核;**价格取决于自家盘口**(§8) |

**② 关联稳定币**

| 项 | 内容 |
|---|---|
| 资产 | USDD |
| 发行方 / 机制 | TRON DAO Reserve 2022-05 发行(⚠ 公开报道称其与 HTX 同一控制人);上线时为算法币,2022-06 脱锚后改称超额抵押,2025 年改为锁 TRX/USDT 铸造(⚠ 沿革为公开报道级) |
| 规模与持有(一手) | 供给 $1.51B,Tron 为主(<https://defillama.com/stablecoin/usdd>);HTX 把它算进 "USDs" 稳定币储备,自有钱包 125M(PoR 页 USDs 明细) |
| 可核性 | 余额可核;**抵押品是 TRX**,与储备主体同一资产 |

**③ 自发包装币**

| 项 | 内容 |
|---|---|
| 资产 | BTC-TRC20(BTCTRON)、HBTC |
| 发行方 / 机制 | BTCTRON:Poloniex 2020 年在 Tron 发行,声称 1:1 赎回,从未披露抵押地址(<https://tronscan.org/#/token20/TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9>);HBTC:火币 2020 年在以太坊发行的包装 BTC,改名 HTX 后停用(<https://etherscan.io/token/0x0316EB71485b0Ab14103307bf65a021042c6d380>) |
| 规模与持有(一手) | BTCTRON 供给 17,545 枚,HTX 持 10,304(58.7%),占其 PoR BTC 行 51%;HBTC 供给仅 969.49 枚,HTX 地址持 ≈540(56%) |
| 可核性 | 余额可核;**在两端的公布地址上均未发现 BTCTRON 抵押物(§7.2,链上检索不能证否);HBTC 发行方自持过半** |

**④ 生息 / 借贷凭证**

| 项 | 内容 |
|---|---|
| 资产 | stUSDT、jUSDT、jUSDD、sTRX(JustLend);stETH(Lido);WBETH(Binance);aEthUSDT(Aave);sUSDS(Sky) |
| 发行方 / 机制 | 把底层资产存进协议后拿到的份额,按底层币记入储备(stUSDT 记作 USDT、stETH 记作 ETH) |
| 规模与持有(一手) | HTX 自有钱包 USDT 中 73% 是 stUSDT(39.55M,§6.2);Poloniex 快照 sUSDS 912.6M、stETH 247.8k(§7);Binance WBETH $8.4B;aEthUSDT 池 09-03 链上:总供给 ≈$29.5 亿、池内现金 $2.36 亿、利用率 92%(<https://etherscan.io/token/0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a>) |
| 可核性 | 余额可核;**能否即时赎回取决于协议里的现金**,所有存款人排同一条队;JustLend 系凭证(<https://tronscan.org/#/token20/TThzxNRLrW2Brp9DcTQU8i4Wd9udCWEdZ3>)的底层又在 JustLend 里,而 JustLend 接受 BTCTRON 作抵押(§7.2) |

- 四类全占的只有 HTX:平台币 + 关联稳定币 + 自发包装币 + 关联协议的生息凭证。
- 聚合器口径剔除 ②③,这正是 §3.2 里 HTX ETH 链"聚合器口径"与"全资产"两列的差额来源。
- 四类里只有 ④ 的非关联部分(stETH、WBETH、sUSDS、aEthUSDT)是"别人的信用",其余都是"自己的信用"。

### 4.4 三条判据逐所对照(关联币占比 ≥10% 的所,及公布逐币负债的所)

| 所 | ① 关联币是储备主体 | ② 盘口:储备持仓 ÷ 主场 ±2% 深度(§8) | ③ 负债端(§5) |
|---|---|---|---|
| HTX | <mark class="r">**是**(77% vs 硬资产 20%)</mark> | TRX ≈180×(十所合计)、HTX 币 ≈880× | 公布逐币负债;**19% 储备在托管方未在页面披露,USDT 自有钱包覆盖负债 5.8%**(§6.2) |
| Bitfinex | 否(32% vs 66%) | LEO ≈90,000× | 无 PoR 页,负债未公布 |
| KuCoin | 否(16% vs 59%) | KCS ≈9,800× | 仅公布比率 110% |
| SwissBorg | 否(15% vs 63%) | 未测 | 无 PoR 页 |
| Binance | 否(15% vs 74%) | BNB ≈2,200× | 公布逐币负债,仅自有钱包 ÷ 负债 100.9% |
| Gate | 否(14% vs 54%) | GT ≈11,000× | 仅公布比率 127% |
| MEXC | 否(11% vs 66%) | 未测 | 仅公布比率 141% |
| OKX | 否(4% vs 86%) | 未测 | 公布逐币负债,103.0% |

**读法**

- ① 只对一家成立。
- ② 对所有测过的所都成立:关联币持仓是主场盘口深度的几百到几万倍,本身不区分谁更危险;它的作用是放大 ①,关联币占比越高,按盘口折算后的储备缩水越多。
- ③ 公布逐币负债的只有 Binance、OKX、HTX 三家;其余要么只给一个比率,要么没有 PoR 页。
- 三条同时成立的所,前 20 名里没有;最接近的是 HTX:① 成立,② 成立(TRX 是这些关联币里盘口最好的,仍为 180 倍),③ 公布了负债,但五分之一储备在托管方未在页面披露。与 FTX 的差别是 TRX 有全市场盘口而 FTT 没有,HTX 公布了负债表而 FTX 没有;相同点是储备价值是自家系代币价格的函数。

## 5. 官方 PoR 横向(各所页面,2026-08-01 快照;第三方托管占储备 >10%、仅自有钱包 ÷ 负债 <100% 标红,与 §10 触发规则一致)

| 所 | 用户负债 | 自报储备 | 第三方托管占储备 | **仅自有钱包 ÷ 负债** |
|---|---|---|---|---|
| Binance | $127.9B | $130.3B | 0.9% | 100.9% |
| OKX(21 资产) | $30.8B | $32.6B | 2.6% | 103.0% |
| HTX | $6.25B | $6.50B | <mark class="r">**19.1%**(托管方不披露)</mark> | <mark class="r">**84.2%**</mark> |
| Gate | — | 127% | 无托管栏 | — |
| Bitget | — | 120%(USDT 100%,零冗余) | 无托管栏 | — |
| KuCoin | — | 110% | 无托管栏 | — |
| MEXC | — | 141% | 无托管栏 | — |
| Kraken | — | 仅比率 | — | — |

## 6. 与自报口径的差异(按所)

同一套读法用在每家所上。本节列的是本报告读到的数与各所自报口径之间的差异,每条附核验方法;本节不设阈值,故不用颜色标注,只加粗差异项。

### 6.1 Binance / Poloniex

| 所 | 差异项 | 读数 | 怎么核 |
|---|---|---|---|
| Binance | 聚合器把锚定代币的抵押储备算进"储备" | **DefiLlama $69.1B 中 $12.3B 来自 lockinfo 的 2 个地址**(USDT 9.18B、USDC 1.58B、ETH 45.5 万),不是用户资产;PoR 37 址本身 $56.4B | `tools/cex_addresses.json` 的 `eth_lock`;`--chain eth --ex binance-cex` |
| Poloniex | 储备构成与集中度 | **"USDT" 94% 是 sUSDS,"ETH" 98% 是 stETH,一个地址占储备 63%**;公布 TRX 地址一个月 −18%(§7.1 逐址) | §7 |

### 6.2 HTX


| # | 差异项 | 读数 | 怎么核 |
|---|---|---|---|
| 1 | **USDT 自有钱包只覆盖负债 5.8%,且其中 73% 是 stUSDT** | 负债 926.3M;"自有钱包" 53.8M = USDT-TRC20 13.24M + USDT-ERC20 1.05M + **stUSDT 39.55M**(JustLend 凭证);655.9M 在"ThirdParty"(76.6%)。官方 USDT-TRC20 5 址链上现值 09-04:**1.91M**(快照 13.24M);USDT-ERC20 现值 0 | HTX PoR 页 "USDs" 明细;GitHub 快照 CSV;`--chain tron --ex htx`(`tron_por` 项) |
| 2 | **19.1% 储备在托管方未在页面披露的第三方托管** | 2026-06-01 起新设类别,含 USDT 656M、USDC 217M、ETH 91.5k、BTC 1,689;Binance 同口径 0.9%、OKX 2.6% | HTX PoR 页 "Custodial Wallets" 栏 |
| 3 | **BTC 储备 51% 是 Poloniex 发行的 BTC-TRC20,公布地址与 PoR 页面上未发现对应抵押物(链上检索不能证否)** | 自报 BTC 20,472 = 原生 8,209 + BTC-TRC20 10,399 + 托管 1,689 + 其他 175;原生链上现值 8,072 = 用户负债 19,933 的 **41%** | `--chain btc,tron --ex htx`;BTC-TRC20 见 §7.2 |
| 4 | **ETH 储备 75% 在托管,链上可核 25.5%** | 页面:用户 122,077 / HTX 122,626 / 交易所钱包 31,101 / 托管 91,525;交易所钱包链上现值 29,374(原生 ETH 仅 112,余为 stETH) | `--chain eth --ex htx`(`eth_por` 项) |
| 5 | **TRX 占储备 47%,69% 质押中,而全市场盘口装不下它的 1%** | 18 址持 9.78B TRX = 供给 10.3%(可用 3.04B + 质押中 6.73B);用户 TRX 负债 8.85B ⇒ 即时可付 34%;十所现货 ±2% 深度合计 $17.6M,HTX 持仓 $3.2B | trongrid `getaccount`;各所深度接口 |
| 6 | **平台币 HTX 计入储备 5.7%,而 HTX 自持其供给 23%,仅本所有成交** | Tron 主链 totalSupply ≈1,000 万亿枚;HTX 18 址持 2.31 万亿;Binance/OKX 未上市,五家挂牌所日成交 $0–5 万;九所无永续 | Tron JSON-RPC;各所行情接口 |
| 7 | **2024-09/10 赎回 95,200 枚 BTC-TRC20,HTX 的真 BTC 不增反减** | HTX 月度快照:09-01 → 11-01 BTC-TRC20 −8,522 枚,原生 BTC −4,762 枚,总 BTC 34,611 → 21,327(−38%);当月 PoR 照报储备率 >100% | HTX GitHub `huobiapi/Tool-Node.js-VerifyAddress` 各 commit 的 CSV |
| 8 | 页面自洽,但可核部分不到一半 | BTC / ETH 页面四个数与 GitHub 快照逐格对上;储备率 102.7% / 100.45% 中,链上能证明"确实是那个币"的部分分别为 41% / 25.5% | 本报告 §3、§5 |

**监管状态(公开记录,不属储备核查的发现)**:英国 FCDO 2026-05-26 列名 Huobi Global S.A.(别名 "HTX (formerly Huobi)"),07-07 更新;欧盟 07 月跟进,08-23 生效;OFAC 未动。来源:FCDO 制裁名单 CSV(一手)。

**同一套脚本、同一天读到的对照组**

- **Binance**:BTC 61 址链上 640,647 枚(0 失败);ETH 37 址 $56.4B;USDT-TRC20 897M。
- **OKX**:ETH 323 址 $12.9B,与聚合器 95%(0 失败);USDT-TRC20 273M。

## 7. Poloniex 与 BTC-TRC20(BTCTRON):HTX 储备中与 Poloniex 关联的部分

**Poloniex**(⚠ 公开报道称 2019 年由与孙宇晨关联的投资团体从 Circle 收购;PoR 地址清单公开于 GitHub `poloniex/tools-nodejs-address-verify`,与 HTX 用同一快照区块高度):

| 项 | 读数 |
|---|---|
| 名义储备(08-01 快照) | $2.73B |
| "USDT" 储备 $968M 的构成 | **94% 是 sUSDS**(Sky 储蓄份额,不是 USDT) |
| "ETH" 储备 252k 的构成 | **98% 是 stETH**,原生 ETH 1,142 |
| 单一地址集中度 | **[`0x176F3DAb…0132`](https://etherscan.io/address/0x176F3DAb24a159341c0509bB36B833E7fdd0a132) 一址持 sUSDS $1.0B + stETH 243k + WBTC 1,690 ≈ $1.72B = 储备的 63%** |
| 链上对账 | BTC 16 址 10,864 → 10,764 ✅;TRX 公布地址一个月 57.8M → 47.3M(−18%,§7.1 逐址) |
| 储备的来源(2026-05-30 起) | 71,993 stETH、806M sUSDS、1,723 WBTC 经 Poloniex 公布地址 `0x8fCA4adE…` → `0x29065a4C…`(Gnosis Safe)转入 Poloniex 9;stETH 上游为 HTX 地址 `0x18709E89…`(逐跳见下) |

**HTX → Poloniex 的资金路径(链上直读,Blockscout 代币转账记录;可用任一浏览器按地址复核)**

- stETH:[`0x18709E89…`](https://etherscan.io/address/0x18709E89BD403F470088aBDAcEbE86CC60dda12e)(HTX 地址,归属依据见下)→ [`0x7C103bbA…`](https://etherscan.io/address/0x7C103bbAE0DA51AE929dE97A98633668ddE80d04)(无标注中转)→ [`0x8fCA4adE…`](https://etherscan.io/address/0x8fCA4adE3a517133fF23ca55CdAea29C78C990b8)(Poloniex PoR 清单内)→ [`0x29065a4C…`](https://etherscan.io/address/0x29065a4C1f2F20d1E263930088890d6F49Fe715a)(Gnosis Safe,Poloniex PoR 清单内)→ Poloniex 9,71,993 枚,全部发生在 2026-05-30。
- sUSDS 200M:05-30 由同一 HTX 地址 `0x18709E89…` → 无标注中转 [`0x7fed2E5e…`](https://etherscan.io/address/0x7fed2E5e06CF7B8918bB93158C4E990794da33b8) → `0x8fCA…` → Safe → Poloniex 9。
- WBTC 1,723:05-30 由 `0x18709E89…` → 无标注中转 [`0xeB245796…`](https://etherscan.io/address/0xeB245796376912af7Fadd4986f73743feEA61e6E) → 同一路径 → Poloniex 9。
- sUSDS 606M:06-04 由无标注中转 [`0x2cf2679A…`](https://etherscan.io/address/0x2cf2679A78771D9f78433D2CdE3690f74e0F6471) → `0x8fCA…` → Safe → Poloniex 9;`0x2cf2…` 的上游是 [`0x93904eeC…`](https://etherscan.io/address/0x93904eeC579e5bF7a57C2DD4AfbEA0F1C3e6A1D1),一个未标注的枢纽地址,自 2026-01 起自行以 USDS 铸出 18.5 亿 sUSDS;其稳定币来源多头,含 HTX 清单地址 `0xa03400E0…` 的小额(USDT 50M、USDC 2.5M、DAI 2.7M),大头来自 Spark 储蓄金库与其他未标注地址。这一路的 HTX 来源未能在链上确立。
- `0x18709E89…` 归属 HTX 的依据(四条独立):①DefiLlama-Adapters 的 `huobi` 项自 2022-11-13 起把它列为 HTX 以太坊地址;②Etherscan 系浏览器在其他 EVM 链(Moonscan、SnowScan)对同一地址的标签为 "Huobi: Recovery";③Hacken 2023-11 对 Heco 桥事件的分析称 HTX 用该地址归集热钱包资金与追回的被盗资金;④链上行为:它向 HTX 官方 PoR 清单里的地址 `0x4fb31291…` 直接转出 LINK、ONDO、FLOKI(2026-07/08),与 HTX 另一清单地址 `0xa03400E0…` 往来百余笔。它不在 HTX 官方 PoR 页公布的 11 个 ETH 地址内。
- 能核实的:三笔资产进入 Poloniex 9 的时间、金额与路径;stETH 71,993、sUSDS 200M、WBTC 1,723 三路的起点都是 HTX 地址 `0x18709E89…`。不能确立的:606M sUSDS 的 HTX 来源(Protos 2026-08 报道,⚠ 媒体级),以及 HTX 的"ThirdParty"栏是否包含这些资产(HTX 不披露托管方)。若包含,同一笔资产会同时出现在 HTX 与 Poloniex 两份 PoR 里。

### 7.1 Poloniex 公布的 TRX 地址:快照 vs 链上,逐址(脚本 `tools/por_trx_delta.py`)

Poloniex 08-01 快照列了 7 个 TRX 地址(另有 1 个 sTRX 地址,即其中的 `TUgSg…`)。地址少,直接逐址列出;表由脚本生成,可重跑。

| 地址 | 快照 TRX | 可用 | 自持质押 | 委托质押/解押中 | 合计 | 变动 | sTRX 现值(快照) | 快照日后 TRX 转出(≥1M) |
|---|---|---|---|---|---|---|---|---|
| [`TWhDfwC8QE…`](https://tronscan.org/#/address/TWhDfwC8QE6pQyiYy248dNor3uphPEw5M2) | 0.52M | 0.26M | 0.00M | 0.00M | 0.26M | -49% | 0.00M(0M) | — |
| [`TUgSgCQL6p…`](https://tronscan.org/#/address/TUgSgCQL6pMSy9zByn4sgxqrJa95sZExBG) | 36.87M | 6.87M | 5.95M | 24.05M | 36.87M | +0% | 39.23M(50M) | — |
| [`TSzSgxRisS…`](https://tronscan.org/#/address/TSzSgxRisS5VBXXDcAezTDvnPGi9CbsXvJ) | 20.39M | 10.16M | 0.00M | 0.00M | 10.16M | -50% | 0.00M(0M) | TWhDfwC8… 11.4M |
| [`TECmrmwPAj…`](https://tronscan.org/#/address/TECmrmwPAjr2RpDGPd4Axq6JYKCESJEhc5) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M(0M) | — |
| [`TVNPqyt6h3…`](https://tronscan.org/#/address/TVNPqyt6h3DV3Pd8N5PmskC96vtbAp863B) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M(0M) | — |
| [`TSmgqvsfx9…`](https://tronscan.org/#/address/TSmgqvsfx95ZpjFRGA2eHhzUFHDhGVzusq) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M(0M) | — |
| [`TV7WmJXhYy…`](https://tronscan.org/#/address/TV7WmJXhYyd4rqRjbWg62eX8e5DoPbyiA3) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M(0M) | — |
| **合计** | **57.78M** | | | | **47.30M** | **-18%** | **39.23M** | |

**读法**

- **一个月净变动 −18%(57.78M → 47.30M)。** `TUgSg…` 上 2,405 万是**委托给他址的质押**(TRX 仍归本址,只是把能量/带宽委托出去;热钱包 `TWhDf…` 的资源正来自它),计入后该址与快照分毫不差。
- 真正减少的是 `TSzSg…`:20.39M → 10.16M,其中 11.45M 转入热钱包 `TWhDf…`;热钱包 08-19 以来发出 8,000+ 笔交易(7,162 笔 USDT 合约调用、838 笔 TRX 转账),是**用户提币通道**。
- `TUgSg…` 的 sTRX 由 50.0M 降到 39.2M,而该地址 08-01 以来**没有发出过任何交易** ⇒ 这 10.8M sTRX 是被已授权的合约划转的,去向未查。
- 一个月内负债端是否同步下降,要等 Poloniex 的 09-01 快照(截至 09-04 GitHub 仍是 08-01 版)。

### 7.2 BTC-TRC20(BTCTRON):合约、持有与抵押物

BTCTRON 是 Poloniex 2020 年在 Tron 链上发行的 "BTC",HTX 的 PoR 把它记作 BTC-TRC20 并计入 BTC 储备。合约 [`TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9`](https://tronscan.org/#/contract/TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9)(tronscan)。下表全部为链上读数。

| 项 | 链上读数 |
|---|---|
| 合约类型 | Tether 式:`issue / redeem / addBlackList / destroyBlackFunds`;owner 为无标签地址 |
| 供给与持有 | 17,545 枚;**[HTX 6](https://tronscan.org/#/address/TDToUxX8sH4z6moQpK3ZLAN24eupu2ivA4) 持 10,304(58.7%)+ [JustLend jBTC 市场](https://tronscan.org/#/contract/TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT) 6,577(37.5%)= 96%**;Poloniex 自持 28 |
| 铸造史 | 铸 114,000 / 销 96,090 / 黑名单销毁 364(闭合);**2022 年铸 89,000 枚当日全部存入 JustLend,非用户提币** |
| 抵押物 | Poloniex PoR 全部 BTC 12,617 枚已对应自己用户负债 12,603 枚;**没有任何一行标为 BTCTRON 储备;16 个 BTC 地址无签名**;2024-09/10 赎回 95,200 枚时,Poloniex 15 个冷址无 ≥1,000 BTC 流出,HTX 原生 BTC 亦未增加 |
| 2022-08-21 | **60,000 枚铸出当日,两个存入地址从 JustLend jUSDC 借出 4 亿 + 6 亿 USDC 转入 Poloniex 签名地址**;jUSDC 池 95% 由借款方关联枢纽供给;2023-07 还清 |
| 当前的借款额度 | JustLend 预言机按真 BTC 全价($76.8k)认 BTCTRON,抵押率 0.75;**一地址 5,000 枚已登记抵押、借款 0、可借 ≈$2.9 亿;jUSDT 池现金 $68M**;另一地址以 200 枚 + sTRX 抵押借着 $16.2M jUSDT |

以上为在 Poloniex 公布地址与其 PoR 页面上**未发现**标记为 BTCTRON 储备的资产。抵押物可能存在于未公布的地址,链上检索无法证否。

## 8. 关联币可变现性:储备中的持仓 ÷ 盘口深度(2026-09-03 实测;关联币占储备 >30%、质押占比 >50% 标红,与 §2/§10 规则一致)

§2 里每家所的"关联币"都按市价计入储备。这一节问同一个问题:**真要卖,盘口接得住多少?** 读法统一:主场 ±2% 盘口深度(挂单可即时成交的美元量)、24h 成交,与储备中该币的持仓相除。

| 所 | 关联币 | 占储备 | 储备中持仓 | 主场 ±2% 深度 | 24h 成交 | 持仓 ÷ 深度 |
|---|---|---|---|---|---|---|
| Binance | BNB | 15% | $24.4B | $10.9M(Binance) | $128M | ≈2,200× |
| Bitfinex | LEO | 33% | $6.3B | $0.07M(Bitfinex) | $0.2M | ≈90,000× |
| Gate | GT | 14% | $0.88B | $0.08M(Gate) | $1.0M | ≈11,000× |
| KuCoin | KCS | 15% | $0.49B | $0.05M(KuCoin) | $1.6M | ≈9,800× |
| Bitget | BGB | 8% | $0.46B | $0.51M(Bitget) | $13.8M | ≈900× |
| HTX | TRX | <mark class="r">47%</mark> | $3.2B(<mark class="r">69% 质押中</mark>) | $17.6M(十所合计;HTX 自家 $0.38M) | $57M(十所) | ≈180× |
| HTX | HTX 币 | 5.7% | $0.37B | $0.42M(六所合计;仅 HTX 有成交) | $7.8M | ≈880× |

**读法**

- 没有一家的关联币能在盘口上出清:持仓是深度的几百到几万倍。**关联币的"储备价值"是市价乘以数量,不是能变现的钱** —— 这对所有所成立,不只 HTX。
- TRX 反而是这些币里相对最"有盘口"的(全市场十所 ±2% $17.6M,永续持仓量 $238M);HTX 的问题不在 TRX 的流动性,在**它占储备的比例(47% + 5.7%)与 69% 的质押** —— Binance 的 BNB 占 15%,其余 73% 是 BTC、ETH 与稳定币;Bitfinex 的 LEO 占 33%,其余 61% 是 BTC。
- 判断一家所压力下的兑付能力,应把关联币按盘口深度而非市价折算后,再看硬资产(BTC / ETH / 稳定币)对负债的覆盖。按此口径(§5 表):Binance、OKX 仍 ≥100%;HTX 的硬资产覆盖不到一半。

## 9. 复现

```bash
pip install curl_cffi
python3 tools/cex_reserves_verify.py --chain all                                    # 三链全量
python3 tools/cex_reserves_verify.py --chain eth --ex okx --retry-failed data/cex_reserves_2026-09-04.json
python3 tools/cex_reserves_verify.py --refresh-addresses                            # 重拉官方地址清单
python3 tools/beacon_validators.py 0x3262f13a39efaca789ae58390441c9ed76bc658a 0xf666814c2ae92ca0e06667f80dac1eb8a97e48ae 0x5c95a672e34b3252482ed9a215f2926d2887845d 0x88a4df73aac310484c60c4c0ac4904cab938c20b   # 按提款地址数信标链验证者(报告 §3.2 Bitstamp)
python3 tools/por_fetch.py                                                          # 各所官方 PoR 自报数(§3.1 末列;Binance 需人工另存页面登记 data/por_manual.json)
```

已知坑(脚本内已规避):公共节点对批量 `eth_call` 静默截断;Tron `eth_getBalance` 不含质押中的 TRX,必须用 `getaccount`;trongrid 免费额度 3 rps,过快会静默降质;Blockscout 对平台币无报价,KCS/GT/BGB 改链上直读。

## 10. 监控指标(同一组指标,逐所读)

下面六个指标对每家所都用同一读法,触发规则相同;读数按 2026-09-03 快照。"—"= 该所无此项(无托管栏、无原生质押币、无关联资产)。

| 指标 | 读法 | 触发 | Binance | OKX | Bitget | Gate | HTX | Poloniex |
|---|---|---|---|---|---|---|---|---|
| 第三方托管占储备 | 官方 PoR 页托管栏 | >10% | 0.9% | 2.6% | — | — | <mark class="r">19.1%</mark> | — |
| 仅自有钱包 ÷ 用户负债 | 官方 PoR 页 | <100% | 100.9% | 103.0% | ≥100%(USDT 恰 100%) | 127% | <mark class="r">84.2%</mark> | ≥100% |
| 稳定币在公布地址上的余额 | `--chain tron/eth`(官方清单) | 主交易稳定币 < 负债 1% | USDT 1,248M(Tron)+ 28.7B(ETH) | 261M + 7.75B | 242M + 569M | 75M + 372M | <mark class="r">1.9M(Tron)+ 0(ETH)</mark>,另 stUSDT 39.6M | 3.9M + 23M |
| 原生币质押占比 | trongrid `getaccount` | >50% | 0% | 0% | 0% | 0% | <mark class="r">69%</mark> | 0%(sTRX 另计) |
| 单一地址占储备 | 各链直读 | >50% | <10% | <10% | <10% | <10% | 32%(TRX 最大址,⚠ 估) | <mark class="r">63%</mark> |
| 关联资产在借贷协议抵押借款 | JustLend `borrowBalance` | 由 0 变非 0 | — | — | — | — | BTCTRON 抵押地址:0(额度 ≈$2.9 亿) | 同左(发行方) |
| 主通道提币状态 | 各所 `currencies` 接口 | 任一 prohibited | 正常 | 正常 | 正常 | 正常 | 正常 | 正常 |

---

**来源等级**

- **一手**:链上直读;官方 PoR 页面与 GitHub 清单;FCDO 制裁名单;各所公开行情接口。
- **第三方**:DefiLlama、CoinGecko。
- **媒体 ⚠**:Protos、TRM Labs 等报道,仅作线索。

---

**免责声明**

本页为公开数据的整理与核对,不构成投资建议,不构成对任何机构偿付能力的断言。负债端数字全部来自交易所自报,本报告无法验证。
