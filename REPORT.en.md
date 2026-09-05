# Top Exchange Reserves Check · 2026-09

> Each table heading carries its own read time. Every number can be re-read with `tools/cex_reserves_verify.py` in this repository; the output snapshot is `data/cex_reserves_2026-09-04.json`.
> Source discipline: **direct on-chain read > official PoR page > public aggregator > media**. The first three go into tables; media is used only as a lead, marked ⚠, and never tabulated.
> This page makes no verdict ("will it fail"); it gives verifiable facts and the gaps between them.

## 0. Conclusions

1. Among top exchanges, **only HTX carries all four kinds of affiliated assets at once**: a platform token (HTX token), an affiliated stablecoin (USDD), self-issued wrapped coins (BTC-TRC20, HBTC), and Sun-system yield receipts (stUSDT/jUSDD). Every other exchange has at most one kind (classification and the three FTX criteria in §4).
2. <mark class="r">HTX reports reserve ratios "all above 100%", but on the on-chain-verifiable basis: own-wallet USDT covers only 5.8% of liabilities, BTC 41%, ETH 25.5%; 19.1% of total reserves sit with an undisclosed "third-party custodian", and 47% is TRX, 69% of which is staked.</mark>
3. Binance / OKX reserves reconcile on the BTC and ETH chains at 99–103%; Bitfinex, Gate, KuCoin and Gemini at 95–101%. **Everyone says "reserve ratio >100%"; the difference is whether it can be seen on chain.**

## 1. Method: three data layers, trust only the bottom one

| Layer | What it is | How this report uses it |
|---|---|---|
| Direct on-chain read | Take the addresses an exchange publishes and read them directly: BTC (mempool.space), ETH with every priced ERC-20 (Blockscout), Tron (trongrid `getaccount`, staking included) | **Primary evidence**; per-address failures are logged in the output JSON |
| Official PoR page | Each exchange's proof-of-reserves page (liabilities, self-reported reserves, custody column) | The only source for the liability side; **this report cannot verify total liabilities** |
| Aggregator (DefiLlama) | Sums over its own address sets. "DefiLlama-Adapters" below means the per-exchange fetch script and address list in its open-source repository of that name (<https://github.com/DefiLlama/DefiLlama-Adapters/tree/main/projects>) | Panorama comparison; two caliber rules below |

**Aggregator caliber rules**

1. Platform tokens are counted; stablecoins issued or affiliated with the exchange (USDD), self-issued wrapped coins (HBTC / BTCTRON) and Aave deposit receipts are not.
2. The Binance row includes the collateral it locks for BSC pegged tokens ($12.3B), which is not customer assets.
3. Address sets may differ from official PoR lists (HTX: 57 DefiLlama-Adapters addresses vs 11 official).

## 2. Panorama: top 20 by on-chain reserves (DefiLlama public-address basis, read 2026-09-04 22:30 UTC)

Sample rule: **the top 20 by on-chain assets on the DefiLlama CEX board**, no discretionary additions or removals; Coinbase / Kraken / Upbit publish no addresses and are not on the board.

- Self-check entry points: the board <https://defillama.com/cexs>; per-exchange pages `https://defillama.com/cex/<slug>` (e.g. <https://defillama.com/cex/htx>, <https://defillama.com/cex/binance-cex>); the API `https://api.llama.fi/protocol/<slug>` (per-chain `currentChainTvls` and token breakdown); DefiLlama-Adapters source <https://github.com/DefiLlama/DefiLlama-Adapters/tree/main/projects> (address lists or fetch logic live there).

- "Affiliated token" = an asset issued by the exchange or its controller; the uniform red rule is **affiliated tokens >30% of reserves**.
- "1-year net flow" = the residual change in reserves after removing price effects (positive = net inflow); price baseline from Binance daily closes: BTC −28.0%, ETH −42.9%, stablecoins 0, affiliated/other ≈ −40%.
- ⚠ The Bitstamp row is the aggregator's 09-04 22:30 UTC read; this report's direct read is 39,951 BTC (§3.1).

| # | Exchange | On-chain reserves | BTC | ETH | Stablecoins | Affiliated | 1-yr net flow |
|---|---|---|---|---|---|---|---|
| 1 | Binance | $167.6B | 31% | 11% | 32% | 15% (BNB) | +13.4% |
| 2 | OKX | $30.0B | 38% | 10% | 38% | 4% (OKB) | +28.6% |
| 3 | Bitfinex | $19.1B | 61% | 3% | 2% | <mark class="r">**32% (LEO)**</mark> | +2.3% |
| 4 | Bybit | $16.0B | 29% | 10% | 36% | 4% (MNT) | -9.7% |
| 5 | Robinhood (broker) | $14.5B | 77% | 21% | 0% | 0% | -1.0% |
| 6 | Gate | $6.8B | 22% | 16% | 16% | 14% (GT) | +12.3% |
| 7 | Bitget | $6.0B | 40% | 7% | 18% | 8% (BGB) | +33.6% |
| 8 | Gemini | $5.3B | 85% | 13% | 0% | 0% | -14.9% |
| 9 | MEXC | $5.3B | 18% | 3% | 45% | 11% (MX) | +51.1% |
| 10 | Deribit | $5.1B | 77% | 11% | 11% | 0% | +28.4% |
| 11 | Bitstamp | $4.7B | 69% | 21% | 1% | 0% | +121.3% ⚠ not an inflow (see reading) |
| 12 | HTX | $3.7B | 18% | 2% | 0% | <mark class="r">**77% (TRX + HT)**</mark> | -10.1% |
| 13 | KuCoin | $3.2B | 20% | 9% | 30% | 16% (KCS) | -12.1% |
| 14 | Crypto.com | $2.5B | 74% | 7% | 9% | 1% (CRO) | -7.1% |
| 15 | HashKey | $1.7B | 65% | 25% | 5% | 0% | +30.8% |
| 16 | Poloniex | $1.5B | 49% | 39% | 1% | 2% (Sun system) | +61.1% ⚠ not customer inflow (see reading and §7) |
| 17 | Bitkub | $1.4B | 65% | 14% | 3% | 0% | +33.6% |
| 18 | SwissBorg | $1.0B | 43% | 14% | 6% | 15% (BORG) | -2.5% |
| 19 | BitMEX | $0.8B | 87% | 0% | 13% | 0% | -60.5% (voluntary shutdown 2026-09-23, withdraw before wind-down) |
| 20 | OSL | $0.7B | 75% | 19% | 3% | 0% | +16.1% |

**How to read**

- Only two exchanges hold more than 30% of reserves in affiliated tokens: **HTX 77%, Bitfinex 32%**. LEO is the platform token iFinex issued in 2019 (not a stablecoin; supported by revenue buybacks and burns), in the same class as BNB, OKB, GT and KCS, and flagged by the same rule.
- The remaining 61% of Bitfinex is BTC.
- Bitstamp +121.3% is not an inflow: the aggregator DefiLlama-Adapters's pagination bug was fixed and its address set completed (DefiLlama-Adapters PR #20878, merged 09-04); its BTC read went from 4,180 to 40,167.
- Poloniex +61.1% is not customer inflow: between 2026-05-30 and 06-04, 71,993 stETH, 806M sUSDS and 1,723 WBTC entered Poloniex 9 (the address holding 63% of its reserves) through two Poloniex-published addresses. The stETH leg traces back to HTX address `0x18709E89…` (attribution verified in §7); the 1,723 WBTC and 200M of the sUSDS trace to the same address; the other 606M sUSDS comes from an unlabelled hub that mints sUSDS itself, and its HTX origin could not be established on chain. Hop by hop in §7.
- The rest of HTX is 18% BTC (half of it the BTC-TRC20 of §7.2) and 2% ETH; there are no stablecoins on the aggregator's address set. Gemini, Bitstamp and Robinhood are also at 0% stablecoins, which is not an anomaly in itself; the read of own-wallet USDT on HTX's official PoR list is in §6.2.

## 3. Direct on-chain reconciliation of published addresses (primary evidence)

§2 is the aggregator's basis; this section is **this report reading the chains itself**: take each exchange's published addresses (official PoR list or DefiLlama-Adapters source, see `tools/cex_addresses.json`), read BTC / all ETH assets / Tron per address, then reconcile against the aggregator. **Tables are generated by `tools/make_tables.py` from `data/cex_reserves_2026-09-04.json`**; every address's read and failure record is in that file.

### 3.1 BTC chain (mempool.space direct read vs aggregator; difference ≤1% green, >5% red)

| Exchange | Addresses (read/total) | Direct BTC | Aggregator BTC | Diff | PoR BTC: users / wallets (snapshot) | Direct − PoR wallets |
|---|---|---|---|---|---|---|
| Binance | 61/61 | 640,647 | 640,647 | <span class="ok">+0.0%</span> | 656,644 / 658,293(08-01) | -2.7% |
| Bitfinex | 3/3 | 146,853 | 146,973 | <span class="ok">-0.1%</span> | — | — |
| Bybit | 25/25 | 58,141 | 58,192 | <span class="ok">-0.1%</span> | 56,438 / 59,064(07-23) | -1.6% |
| Gate | 13/13 | 18,704 | 19,040 | -1.8% | 22,436 / 27,550(08-19) | <mark class="r">-32.1%</mark>(the 13-address DefiLlama-Adapters list is not every wallet on the page (Gate publishes no BTC addresses)) |
| Bitget | 19/19 | 29,579 | 29,540 | <span class="ok">+0.1%</span> | 26,811 / 35,837(08-20) | <mark class="r">-17.5%</mark>(the 19-address adapter list is not every wallet on the page; page wallets include 535 BTC on BSC/Lightning etc.) |
| MEXC | 34/34 | 11,732 | 11,741 | <span class="ok">-0.1%</span> | 4,282 / 12,313(08-09) | -4.7% |
| Gemini | 4/4 | 56,351 | 56,396 | <span class="ok">-0.1%</span> | — | — |
| Deribit | 17/17 | 49,431 | 49,326 | <span class="ok">+0.2%</span> | — | — |
| HTX | 11/11 | 8,376 | 8,280 | +1.2% | 19,933 / 20,472(08-01) | <mark class="r">-59.1%</mark>(reported wallet includes BTC-TRC20 10,399 + custody 1,689 + BTC-SOL/jWBTC 175; native 8,209 vs direct read +2%) |
| Crypto.com | 8/8 | 22,722 | 22,739 | <span class="ok">-0.1%</span> | — | — |
| Bitstamp | 507/507 | 39,951 | 41,125 | -2.9% | — | — |

**How to read**

- **All eleven reconcile** (difference ≤1.2%); the aggregator's BTC figures can be cited directly.
- The HTX row is the DefiLlama-Adapters's 11-address list; its official PoR list has 7 addresses holding 8,072 BTC on chain (§6.2).
- The Gate list once contained 3 strings starting with `3P` that returned 404 on both BTC explorers; decoded, they are not Bitcoin addresses (35 characters, checksum fails) but Waves-chain addresses from the `waves` section of the DefiLlama-Adapters (Waves mainnet addresses happen to start with 3P), mis-sorted into BTC by prefix when this report extracted them. They are removed, and the script now validates addresses.
- The last two columns: each exchange's self-reported BTC from its official PoR page (user liabilities / exchange wallets incl. custody; fetched by `tools/por_fetch.py`, Binance and Bybit entered manually), and the direct read's difference from the reported wallets (percent). Differences over 5% are red with the reason: they come from snapshot dates, address sets (the DefiLlama-Adapters address list is not every wallet on the page) and caliber (HTX counts BTC-TRC20 and custody as wallets), and are not a reserve-anomaly criterion. OKX (134,399 / 148,552, 08-11) and KuCoin (7,441 / 7,985, 08-31) self-report BTC but publish no BTC addresses, so they are not in the table. Bitfinex, Gemini and Bitstamp have no Merkle PoR page and report no per-coin figures; Deribit stopped publishing PoR on 2026-09-01 (90% of client assets moved to Coinbase custody); Crypto.com has a page but its figures are script-rendered and no snapshot has been taken yet.

### 3.2 ETH chain (Blockscout all-asset direct read vs aggregator; the "aggregator-caliber" column excludes USDD/HBTC/aEthUSDT; coverage 95–105% green, <90% or >110% red)

| Exchange | Addresses | All-asset read | Aggregator-caliber read | Aggregator | Coverage | Failed | PoR ETH: users / wallets (snapshot) |
|---|---|---|---|---|---|---|---|
| Binance | 37 + lock 2 | $68.70B | $68.69B | $69.16B | <span class="ok">99%</span> | 0 | ? / 3,991,221(08-01) |
| OKX | 323 | $12.90B | $12.90B | $13.52B | <span class="ok">95%</span> | 0 | 1,725,703 / 1,749,426(Aug 2026) |
| Bitfinex | 9 | $7.15B | $7.15B | $7.06B | <span class="ok">101%</span> | 0 | — |
| Gate | 91 | $3.03B | $3.03B | $3.01B | <span class="ok">101%</span> | 0 | 375,430 / 458,203(08-19) |
| Bitget | 80 | $1.59B | $1.59B | $1.65B | <span class="ok">96%</span> | 0 | 123,688 / 190,090(08-20) |
| Gemini | 5 | $0.78B | $0.78B | $0.79B | <span class="ok">98%</span> | 0 | — |
| HTX | 57 | $0.22B | $0.13B | $0.12B | 108% | 0 | 122,077 / 122,627(08-01) |
| KuCoin | 96 | $1.59B | $1.59B | $1.60B | <span class="ok">99%</span> | 0 | 101,664 / 118,497(08-31) |
| Bitstamp | 64 | $0.59B | $0.59B | $1.15B | <mark class="n">51%*</mark> | 0 | — |

**How to read**

- **Eight exchanges at 95–101%**; the aggregator can be cited.
- HTX's all-asset read of $0.22B exceeds the aggregator's $0.12B; the gap is exactly USDD $45M + HBTC $42M. The aggregator excludes exchange-issued or affiliated assets (§1 rules); on the same caliber it is 108%.
- \* Bitstamp 51%: a caliber difference, not an address difference. DefiLlama counts all Beacon-chain staked ETH whose withdrawal credentials point to Bitstamp addresses (≈233k ETH, 8,011 validators) as Bitstamp reserves; this report does not, because staked ETH sits on no published address's balance, and two of the four withdrawal addresses are not on Bitstamp's published list, so the attribution rests on the aggregator's own address table alone. Adding that part back, the two sides reconcile. Independent check: `tools/beacon_validators.py` (§9).
- The Binance row includes 2 pegged-token lock addresses ($12.3B), not customer assets. "Pegged-token lock" means the native collateral Binance locks on Ethereum mainnet for the Binance-Peg tokens it issues on BNB Chain (BSC versions of USDT, USDC, ETH, etc.); the liability side is the holders of those pegged tokens, not exchange customers. The addresses come from Binance's lockinfo endpoint and are not on its PoR list; a proposal to split them out has been filed with the aggregator (DefiLlama-Adapters PR #20885, pending maintainers).
- "Failed addresses" are all 0 (one OKX address cleared after a retry).
- The last column is each exchange's self-reported ETH (users / wallets, snapshot dates vary). Its caliber is **ETH across all chains** (L2s, staking receipts and custody included), not the same as this table's Ethereum-mainnet dollar read, so it is shown for reference only and no difference is computed.

### 3.3 Tron chain (trongrid `getaccount` with four staking buckets + direct USDT-TRC20 read)

| Exchange | Addresses | TRX available | TRX staked | USDT-TRC20 | PoR TRX: users / wallets | PoR USDT (all chains): users / wallets |
|---|---|---|---|---|---|---|
| Binance | 25 | 2,287M | 0M | 897.1M | — | — |
| OKX | 23 | 107M | 0M | 273.2M | — | 8,118M / 8,637M(Aug 2026) |
| Bitfinex | 2 | 28M | 0M | 76.8M | — | — |
| Gate | 11 | 15M | 0M | 63.7M | 58M / 179M(08-19) | 660M / 721M(08-19) |
| Bitget | 29 | 5M | 0M | 254.1M | — | 1,454M / 1,456M(08-20) |
| HTX | 18 | 3,046M | 6,646M | 0.0M | ? / 9,376M(08-01) | 926M / 710M(08-01) |
| KuCoin | 24 | 14M | 0M | 148.7M | — | 955M / 1,059M(08-31) |

**How to read**

- **The aggregator cannot be cited here.** It misses USDT-TRC20 (Bitget's published addresses hold 242M, the aggregator records 0), and its `eth_getBalance` read excludes staked TRX.
- Tron's "freeze" is its official term for staking TRX with the network in exchange for bandwidth, energy and votes: ownership is unchanged, unstaking can be started at any time and lands 14 days later; it is neither loan collateral nor a platform or judicial freeze. This report says "staked" throughout. Staked TRX can be in four places: V1 stake, V2 self-held stake, **stake delegated to other addresses** (the TRX still belongs to the address), and the unstaking queue; the "TRX staked" column counts all four. OKX's 520M and Poloniex's 24M are delegated stake, invisible if you only read `balance + frozenV2` (§7.1).
- HTX's 18 Tron addresses in the table are the DefiLlama-Adapters's TRX cold wallets; holding no USDT there is normal. **HTX's official PoR has 5 separate USDT-TRC20 addresses**: 13.24M in the 08-01 snapshot, <mark class="r">1.91M</mark> on chain on 09-04 (the 11.33M on `TK86…` has been emptied); the single USDT-ERC20 address went 1.05M → 0. The rest of the 926M user USDT liability sits in "ThirdParty" (§6.2).
- The last two columns are each exchange's self-reported TRX and USDT (users / wallets); USDT is the **all-chain total** (ERC20 + TRC20 + others) while this table's USDT-TRC20 is one chain, so no difference is computed. HTX's reported TRX wallets of 9,376M are in the same range as this table's 9,692M across 18 addresses (available + staked); of its reported 710M USDT wallets, 656M sit in "ThirdParty" (§6.2).

## 4. Affiliated tokens as a share of reserves: FTX's structural preconditions, and who meets them

### 4.1 What FTX's structural preconditions were (⚠ public reporting, used only as the source of the criteria)

FTX's balance-sheet structure before its November 2022 collapse is where this chapter's criteria come from. Three points:

- **Its own token was the bulk of assets**: on 2022-11-02 CoinDesk published the balance sheet of Alameda, FTX's affiliated market maker: of $14.6B in assets, $3.66B was FTX's platform token FTT and another $2.16B was "FTT collateral"; FTT-related items exceeded a third of assets (<https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet>).
- **Its own token had no order book**: most of the FTT float sat with FTX and Alameda themselves; market cap was list price times quantity, not money that could be realised. On 11-06 Binance announced it would sell its FTT, and FTT lost 80% over the next three days.
- **The liability side was opaque**: customer deposits had been diverted to Alameda, and outsiders could not see how liabilities matched assets; withdrawals were halted on 11-08 and bankruptcy filed on 11-11.

The criterion: **what is fatal is not "holding your own token", it is all three at once** — ① the own token is the bulk of reserves; ② the own token has no order book; ③ the liability side is opaque. Below, every exchange is checked against the same rules.

### 4.2 By exchange: affiliated tokens as a share of reserves (data as in §2; red rule as in §2: affiliated >30% of reserves)

"Hard assets" = BTC + ETH + stablecoins; whatever the two columns leave short of 100% is other coins (SOL, XRP, etc.).

| Exchange | Affiliated token | Share of reserves | Hard assets |
|---|---|---|---|
| HTX | TRX + HTX token | <mark class="r">**77%**</mark> | 20% |
| Bitfinex | LEO | <mark class="r">**32%**</mark> | 66% |
| KuCoin | KCS | 16% | 59% |
| SwissBorg | BORG | 15% | 63% |
| Binance | BNB | 15% | 74% |
| Gate | GT | 14% | 54% |
| MEXC | MX | 11% | 66% |
| Bitget | BGB | 8% | 65% |
| OKX | OKB | 4% | 86% |
| Bybit | MNT | 4% | 75% |
| Poloniex | Sun-system tokens | 2% | 89% |
| Crypto.com | CRO | 1% | 90% |
| Robinhood, Gemini, Deribit, Bitstamp, HashKey, Bitkub, BitMEX, OSL | — | 0% | 77–100% |

- Two exchanges are above 30%: HTX 77%, Bitfinex 32%. The difference is in hard assets: Bitfinex holds 66% hard assets, twice its LEO; HTX holds 20%, with affiliated tokens nearly four times that. Whether affiliated tokens exceed hard assets is the basis of criterion ① in §4.4.
- The table above is on the aggregator's basis (published addresses only, self-issued/affiliated assets excluded). On HTX's own PoR snapshot basis (§5, §6.2): TRX is 47%, HTX token 5.7%, and 51% of the BTC line is the Poloniex-issued BTC-TRC20 (§7).

### 4.3 Affiliated assets by nature: four kinds

The table above is arranged by exchange; below is arranged by asset, one block per kind. One exchange's affiliated assets can span all four.

**① Platform tokens**

| Item | Detail |
|---|---|
| Assets | BNB, LEO, OKB, GT, KCS, BGB, MX, MNT, CRO, BORG, HTX token |
| Issuer / mechanism | Issued by the exchange itself; value = the exchange's own credit |
| Size and holdings (primary) | LEO $6.3B in Bitfinex reserves; HTX holds 23% of the HTX token supply itself, and it trades only on HTX (§6.2, §8) |
| Verifiability | Balances verifiable; **price depends on the exchange's own order book** (§8) |

**② Affiliated stablecoin**

| Item | Detail |
|---|---|
| Assets | USDD |
| Issuer / mechanism | Issued 2022-05 by TRON DAO Reserve, same controller as HTX; launched as an algorithmic coin, restyled "over-collateralised" after the 2022-06 depeg, and in 2025 changed to minting against locked TRX/USDT (⚠ history from public reporting) |
| Size and holdings (primary) | Supply $1.51B, mostly on Tron (<https://defillama.com/stablecoin/usdd>); HTX counts it in its "USDs" stablecoin reserves, 125M in own wallets (PoR page USDs breakdown) |
| Verifiability | Balances verifiable; **the collateral is TRX**, the same asset as the bulk of the reserves |

**③ Self-issued wrapped coins**

| Item | Detail |
|---|---|
| Assets | BTC-TRC20 (BTCTRON), HBTC |
| Issuer / mechanism | BTCTRON: issued by Poloniex on Tron in 2020, claims 1:1 redemption, has never disclosed a collateral address (<https://tronscan.org/#/token20/TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9>); HBTC: wrapped BTC issued by Huobi on Ethereum in 2020, discontinued after the rebrand to HTX (<https://etherscan.io/token/0x0316EB71485b0Ab14103307bf65a021042c6d380>) |
| Size and holdings (primary) | BTCTRON supply 17,545, HTX holds 10,304 (58.7%), 51% of its PoR BTC line; HBTC supply only 969.49, HTX addresses hold ≈540 (56%) |
| Verifiability | Balances verifiable; **BTCTRON collateral cannot be found at either end (§7.2); the HBTC issuer holds more than half of it itself** |

**④ Yield / lending receipts**

| Item | Detail |
|---|---|
| Assets | stUSDT, jUSDT, jUSDD, sTRX (JustLend); stETH (Lido); WBETH (Binance); aEthUSDT (Aave); sUSDS (Sky) |
| Issuer / mechanism | Shares received for depositing the underlying into a protocol, booked in reserves as the underlying (stUSDT as USDT, stETH as ETH) |
| Size and holdings (primary) | 73% of HTX's own-wallet USDT is stUSDT (39.55M, §6.2); Poloniex snapshot sUSDS 912.6M, stETH 247.8k (§7); Binance WBETH $8.4B; the aEthUSDT pool on chain 09-03: total supply ≈$2.95B, cash in pool $236M, utilisation 92% (<https://etherscan.io/token/0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a>) |
| Verifiability | Balances verifiable; **instant redemption depends on the cash in the protocol**, and every depositor stands in the same queue; the underlying of JustLend receipts (<https://tronscan.org/#/token20/TThzxNRLrW2Brp9DcTQU8i4Wd9udCWEdZ3>) is itself inside JustLend, and JustLend accepts BTCTRON as collateral (§7.2) |

- Only HTX has all four kinds: platform token + affiliated stablecoin + self-issued wrapped coins + yield receipts from a protocol under the same controller.
- The aggregator's basis excludes ② and ③, which is exactly the gap between the "aggregator-caliber" and "all-asset" columns for HTX's ETH chain in §3.2.
- Of the four kinds, only the non-affiliated part of ④ (stETH, WBETH, sUSDS, aEthUSDT) is "someone else's credit"; everything else is "own credit".

### 4.4 The three criteria, exchange by exchange (exchanges with affiliated ≥10%, plus those publishing per-coin liabilities)

| Exchange | ① Affiliated = bulk of reserves | ② Holding ÷ home-venue ±2% depth (§8) | ③ Liability side (§5) |
|---|---|---|---|
| HTX | <mark class="r">**Yes** (77% vs hard assets 20%)</mark> | TRX ≈180× (ten venues combined), HTX token ≈880× | Publishes per-coin liabilities; <mark class="r">19% of reserves with an undisclosed custodian, own-wallet USDT covers 5.8% of liabilities</mark> (§6.2) |
| Bitfinex | No (32% vs 66%) | LEO ≈90,000× | No PoR page, liabilities unpublished |
| KuCoin | No (16% vs 59%) | KCS ≈9,800× | Ratio only, 110% |
| SwissBorg | No (15% vs 63%) | Not measured | No PoR page |
| Binance | No (15% vs 74%) | BNB ≈2,200× | Publishes per-coin liabilities; own wallets ÷ liabilities 100.9% |
| Gate | No (14% vs 54%) | GT ≈11,000× | Ratio only, 127% |
| MEXC | No (11% vs 66%) | Not measured | Ratio only, 141% |
| OKX | No (4% vs 86%) | Not measured | Publishes per-coin liabilities, 103.0% |

**How to read**

- ① holds for one exchange only.
- ② holds for every exchange measured: affiliated holdings are hundreds to tens of thousands of times the home-venue depth. On its own it does not rank danger; its role is to amplify ①. The higher the affiliated share, the more the reserves shrink once marked to order-book depth.
- ③ Only Binance, OKX and HTX publish per-coin liabilities; the rest either give a single ratio or have no PoR page.
- Of the top 20, only HTX comes close to all three at once: ① holds, ② holds (TRX has the best order book of these tokens, still 180×), ③ liabilities are published but a fifth of reserves sit with an undisclosed custodian. The differences from FTX: TRX has a market-wide order book and FTT did not; HTX publishes a liability sheet and FTX did not. The similarity: reserve value is a function of the price of its own family of tokens.

## 5. Official PoR side by side (each exchange's page, 2026-08-01 snapshot)

| Exchange | User liabilities | Reported reserves | Third-party custody share | **Own wallets ÷ liabilities** |
|---|---|---|---|---|
| Binance | $127.9B | $130.3B | 0.9% | 100.9% |
| OKX (21 assets) | $30.8B | $32.6B | 2.6% | 103.0% |
| HTX | $6.25B | $6.50B | <mark class="r">**19.1%** (custodian undisclosed)</mark> | <mark class="r">**84.2%**</mark> |
| Gate | — | 127% | no custody column | — |
| Bitget | — | 120% (USDT 100%, zero surplus) | no custody column | — |
| KuCoin | — | 110% | no custody column | — |
| MEXC | — | 141% | no custody column | — |
| Kraken | — | ratio only | — | — |

## 6. Anomaly list (by exchange)

The same reading is applied to every exchange; red marks what this report identifies as an anomaly, each with its verification method.

### 6.1 Binance / Poloniex

| Exchange | Anomaly | Reading | How to verify |
|---|---|---|---|
| Binance | The aggregator counts pegged-token collateral as "reserves" | <mark class="r">$12.3B of DefiLlama's $69.1B comes from 2 lockinfo addresses</mark> (USDT 9.18B, USDC 1.58B, ETH 455k), not customer assets; the 37 PoR addresses alone hold $56.4B | `eth_lock` in `tools/cex_addresses.json`; `--chain eth --ex binance-cex` |
| Poloniex | Reserve composition and concentration | <mark class="r">94% of "USDT" is sUSDS, 98% of "ETH" is stETH, one address holds 63% of reserves</mark>; published TRX addresses −18% in a month (§7.1 per address) | §7 |

### 6.2 HTX


| # | Anomaly | Reading | How to verify |
|---|---|---|---|
| 1 | <mark class="r">Own-wallet USDT covers only 5.8% of liabilities, and 73% of that is stUSDT</mark> | Liabilities 926.3M; "own wallets" 53.8M = USDT-TRC20 13.24M + USDT-ERC20 1.05M + **stUSDT 39.55M** (JustLend receipt); 655.9M in "ThirdParty" (76.6%). The 5 official USDT-TRC20 addresses on chain 09-04: <mark class="r">1.91M</mark> (snapshot 13.24M); USDT-ERC20 now 0 | HTX PoR page "USDs" breakdown; GitHub snapshot CSV; `--chain tron --ex htx` (`tron_por` item) |
| 2 | <mark class="r">19.1% of reserves in third-party custody with undisclosed identity</mark> | Category added 2026-06-01, holding USDT 656M, USDC 217M, ETH 91.5k, BTC 1,689; Binance 0.9% and OKX 2.6% on the same basis | HTX PoR page "Custodial Wallets" column |
| 3 | <mark class="r">51% of BTC reserves is Poloniex-issued BTC-TRC20, with no collateral found on chain</mark> | Reported BTC 20,472 = native 8,209 + BTC-TRC20 10,399 + custody 1,689 + other 175; native on chain now 8,072 = **41%** of the 19,933 user liability | `--chain btc,tron --ex htx`; BTC-TRC20 in §7.2 |
| 4 | <mark class="r">75% of ETH reserves in custody, 25.5% verifiable on chain</mark> | Page: users 122,077 / HTX 122,626 / exchange wallets 31,101 / custody 91,525; exchange wallets on chain now 29,374 (native ETH only 112, the rest stETH) | `--chain eth --ex htx` (`eth_por` item) |
| 5 | <mark class="r">TRX is 47% of reserves, 69% staked, and the whole market's order book cannot absorb 1% of it</mark> | 18 addresses hold 9.78B TRX = 10.3% of supply (3.04B available + 6.73B staked); user TRX liability 8.85B ⇒ 34% payable at once; ±2% spot depth across ten venues $17.6M in total, HTX holding $3.2B | trongrid `getaccount`; each venue's depth API |
| 6 | <mark class="r">The HTX platform token is 5.7% of reserves, while HTX holds 23% of its supply and it trades only on HTX</mark> | Tron mainnet totalSupply ≈1,000 trillion; HTX's 18 addresses hold 2.31 trillion; not listed on Binance/OKX, daily volume on the five listing venues $0–50k; no perpetuals on nine venues | Tron JSON-RPC; each venue's market API |
| 7 | <mark class="r">95,200 BTC-TRC20 redeemed in 2024-09/10, yet HTX's real BTC fell rather than rose</mark> | HTX monthly snapshots 09-01 → 11-01: BTC-TRC20 −8,522, native BTC −4,762, total BTC 34,611 → 21,327 (−38%); that month's PoR still reported a ratio >100% | CSVs in each commit of HTX's GitHub `huobiapi/Tool-Node.js-VerifyAddress` |
| 8 | <mark class="r">Listed on UK and EU Russia-related sanctions lists</mark> | UK FCDO listed Huobi Global S.A. (alias "HTX (formerly Huobi)") on 2026-05-26, updated 07-07; the EU followed in July, effective 08-23; OFAC has not acted | FCDO sanctions list CSV (primary) |
| 9 | Page is internally consistent, but less than half is verifiable | The four BTC / ETH figures on the page match the GitHub snapshot cell by cell; of the reported 102.7% / 100.45% ratios, the share provably "that coin" on chain is 41% / 25.5% | §3 and §5 of this report |

**Control group read with the same scripts on the same day**

- **Binance**: 61 BTC addresses, 640,647 BTC on chain (0 failures); 37 ETH addresses $56.4B; USDT-TRC20 897M.
- **OKX**: 323 ETH addresses $12.9B, 95% of the aggregator (0 failures); USDT-TRC20 273M.

## 7. Poloniex and BTC-TRC20 (BTCTRON): the other half of the HTX reserve story

**Poloniex** (controlled by Justin Sun since 2019; PoR address list published on GitHub `poloniex/tools-nodejs-address-verify`, same snapshot block height as HTX):

| Item | Reading |
|---|---|
| Nominal reserves (08-01 snapshot) | $2.73B |
| Composition of the $968M "USDT" reserve | <mark class="r">94% is sUSDS</mark> (Sky savings shares, not USDT) |
| Composition of the 252k "ETH" reserve | <mark class="r">98% is stETH</mark>, native ETH 1,142 |
| Single-address concentration | <mark class="r">[`0x176F3DAb…0132`](https://etherscan.io/address/0x176F3DAb24a159341c0509bB36B833E7fdd0a132) alone holds sUSDS $1.0B + stETH 243k + WBTC 1,690 ≈ $1.72B = 63% of reserves</mark> (⚠ Etherscan labelled this address "Justin Sun 4" in 2023; media grade) |
| On-chain reconciliation | BTC 16 addresses 10,864 → 10,764 ✅; published TRX addresses 57.8M → 47.3M in a month (−18%, §7.1 per address) |
| Where the reserves came from (from 2026-05-30) | 71,993 stETH, 806M sUSDS and 1,723 WBTC entered Poloniex 9 via the Poloniex-published addresses `0x8fCA4adE…` → `0x29065a4C…` (Gnosis Safe); the stETH originates from HTX address `0x18709E89…` (hops below) |

**The HTX → Poloniex fund path (direct on-chain read of Blockscout token transfers; verifiable by address in any explorer)**

- stETH: [`0x18709E89…`](https://etherscan.io/address/0x18709E89BD403F470088aBDAcEbE86CC60dda12e) (HTX address, attribution below) → [`0x7C103bbA…`](https://etherscan.io/address/0x7C103bbAE0DA51AE929dE97A98633668ddE80d04) (unlabelled pass-through) → [`0x8fCA4adE…`](https://etherscan.io/address/0x8fCA4adE3a517133fF23ca55CdAea29C78C990b8) (on Poloniex's PoR list) → [`0x29065a4C…`](https://etherscan.io/address/0x29065a4C1f2F20d1E263930088890d6F49Fe715a) (Gnosis Safe, on Poloniex's PoR list) → Poloniex 9, 71,993 stETH, all on 2026-05-30.
- sUSDS 200M: on 05-30 from the same HTX address `0x18709E89…` → unlabelled pass-through [`0x7fed2E5e…`](https://etherscan.io/address/0x7fed2E5e06CF7B8918bB93158C4E990794da33b8) → `0x8fCA…` → Safe → Poloniex 9.
- WBTC 1,723: on 05-30 from `0x18709E89…` → unlabelled pass-through [`0xeB245796…`](https://etherscan.io/address/0xeB245796376912af7Fadd4986f73743feEA61e6E) → the same path → Poloniex 9.
- sUSDS 606M: on 06-04 from unlabelled pass-through [`0x2cf2679A…`](https://etherscan.io/address/0x2cf2679A78771D9f78433D2CdE3690f74e0F6471) → `0x8fCA…` → Safe → Poloniex 9; upstream of `0x2cf2…` is [`0x93904eeC…`](https://etherscan.io/address/0x93904eeC579e5bF7a57C2DD4AfbEA0F1C3e6A1D1), an unlabelled hub that has minted 1.85B sUSDS from USDS itself since 2026-01; its stablecoin inflows are many-sourced, including small amounts from HTX list address `0xa03400E0…` (USDT 50M, USDC 2.5M, DAI 2.7M), with the bulk from a Spark savings vault and other unlabelled addresses. The HTX origin of this leg could not be established on chain.
- Attribution of `0x18709E89…` to HTX rests on four independent grounds: ① the `huobi` entry of DefiLlama-Adapters has listed it as an HTX Ethereum address since 2022-11-13; ② Etherscan-family explorers on other EVM chains (Moonscan, SnowScan) label the same address "Huobi: Recovery"; ③ Hacken's 2023-11 analysis of the Heco bridge incident describes HTX using it to consolidate hot-wallet funds and recovered stolen funds; ④ on-chain behaviour: it sends LINK, ONDO and FLOKI directly to `0x4fb31291…`, an address on HTX's official PoR list (2026-07/08), and has over a hundred transfers with HTX list address `0xa03400E0…`. It is not among the 11 ETH addresses on HTX's official PoR page.
- Verified: the timing, amounts and path of the three inflows into Poloniex 9; the stETH 71,993, sUSDS 200M and WBTC 1,723 legs all start at HTX address `0x18709E89…`. Not established: the HTX origin of the 606M sUSDS (Protos, 2026-08, ⚠ media grade), and whether HTX's "ThirdParty" column includes these assets (HTX does not disclose its custodian). If it does, the same assets appear in both the HTX and Poloniex PoR.

### 7.1 Poloniex's published TRX addresses: snapshot vs chain, per address (script `tools/por_trx_delta.py`)

Poloniex's 08-01 snapshot lists 7 TRX addresses (plus 1 sTRX address, which is the `TUgSg…` among them). Few enough to list one by one; the table is script-generated and can be re-run.

| Address | Snapshot TRX | Available | Own stake | Delegated / unstaking | Total | Change | sTRX now (snapshot) | Sent out after snapshot (≥1M) |
|---|---|---|---|---|---|---|---|---|
| [`TWhDfwC8QE…`](https://tronscan.org/#/address/TWhDfwC8QE6pQyiYy248dNor3uphPEw5M2) | 0.52M | 0.26M | 0.00M | 0.00M | 0.26M | -49% | 0.00M (0M) | — |
| [`TUgSgCQL6p…`](https://tronscan.org/#/address/TUgSgCQL6pMSy9zByn4sgxqrJa95sZExBG) | 36.87M | 6.87M | 5.95M | 24.05M | 36.87M | +0% | 39.23M (50M) | — |
| [`TSzSgxRisS…`](https://tronscan.org/#/address/TSzSgxRisS5VBXXDcAezTDvnPGi9CbsXvJ) | 20.39M | 10.16M | 0.00M | 0.00M | 10.16M | -50% | 0.00M (0M) | TWhDfwC8… 11.4M |
| [`TECmrmwPAj…`](https://tronscan.org/#/address/TECmrmwPAjr2RpDGPd4Axq6JYKCESJEhc5) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M (0M) | — |
| [`TVNPqyt6h3…`](https://tronscan.org/#/address/TVNPqyt6h3DV3Pd8N5PmskC96vtbAp863B) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M (0M) | — |
| [`TSmgqvsfx9…`](https://tronscan.org/#/address/TSmgqvsfx95ZpjFRGA2eHhzUFHDhGVzusq) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M (0M) | — |
| [`TV7WmJXhYy…`](https://tronscan.org/#/address/TV7WmJXhYyd4rqRjbWg62eX8e5DoPbyiA3) | 0.00M | 0.00M | 0.00M | 0.00M | 0.00M | +0% | 0.00M (0M) | — |
| **Total** | **57.78M** | | | | **47.30M** | **-18%** | **39.23M** | |

**How to read**

- **Net change over the month −18% (57.78M → 47.30M).** The 24.05M on `TUgSg…` is **stake delegated to other addresses** (the TRX still belongs to it; only energy/bandwidth is delegated out, and the hot wallet `TWhDf…` gets its resources from it). Counting it, that address matches the snapshot exactly.
- The real decrease is `TSzSg…`: 20.39M → 10.16M, of which 11.45M went to the hot wallet `TWhDf…`; the hot wallet has sent 8,000+ transactions since 08-19 (7,162 USDT contract calls, 838 TRX transfers) and is **the user withdrawal channel**.
- The sTRX on `TUgSg…` fell from 50.0M to 39.2M while that address **has sent no transaction since 08-01** ⇒ the 10.8M sTRX was moved by an already-approved contract; destination not traced.
- Whether the liability side fell in step over the month has to wait for Poloniex's 09-01 snapshot (as of 09-04 GitHub still shows the 08-01 version).

### 7.2 BTC-TRC20 (BTCTRON): contract, holders and collateral

BTCTRON is the "BTC" Poloniex issued on Tron in 2020; HTX's PoR books it as BTC-TRC20 inside its BTC reserves. Contract [`TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9`](https://tronscan.org/#/contract/TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9) (tronscan). Everything in the table is an on-chain read.

| Item | On-chain reading |
|---|---|
| Contract type | Tether-style: `issue / redeem / addBlackList / destroyBlackFunds`; owner is an unlabelled address |
| Supply and holders | 17,545; <mark class="r">[HTX 6](https://tronscan.org/#/address/TDToUxX8sH4z6moQpK3ZLAN24eupu2ivA4) holds 10,304 (58.7%) + [JustLend jBTC market](https://tronscan.org/#/contract/TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT) 6,577 (37.5%) = 96%</mark>; Poloniex itself holds 28 |
| Mint history | Minted 114,000 / redeemed 96,090 / blacklist-burned 364 (closes); <mark class="r">the 89,000 minted in 2022 went straight into JustLend the same day, not to user withdrawals</mark> |
| Collateral | All 12,617 BTC in Poloniex's PoR already correspond to its own 12,603 user liability; <mark class="r">no line is marked as BTCTRON reserve; the 16 BTC addresses carry no signature</mark>; when 95,200 were redeemed in 2024-09/10, none of Poloniex's 15 cold addresses showed an outflow ≥1,000 BTC and HTX's native BTC did not rise |
| 2022-08-21 | <mark class="r">The day 60,000 were minted, the two deposit addresses borrowed 400M + 600M USDC from JustLend jUSDC and sent it to a Poloniex signing address</mark>; 95% of the jUSDC pool was supplied by hubs affiliated with the borrower; repaid 2023-07 |
| Today's credit line | The JustLend oracle prices BTCTRON at full real-BTC price ($76.8k), collateral factor 0.75; <mark class="r">one address has 5,000 registered as collateral, borrow 0, borrowable ≈$290M; jUSDT pool cash $68M</mark>; another address borrows $16.2M jUSDT against 200 + sTRX |

## 8. Realisability of affiliated tokens: reserve holdings ÷ order-book depth (measured 2026-09-03)

In §2 every exchange's "affiliated token" enters reserves at market price. This section asks the same question of each: **if it had to be sold, how much could the order book take?** Uniform reading: home-venue ±2% depth (dollar amount fillable at once), 24h volume, divided into the reserve holding of that token.

| Exchange | Token | Share | Reserve holding | ±2% depth (home venue) | 24h volume | Holding ÷ depth |
|---|---|---|---|---|---|---|
| Binance | BNB | 15% | $24.4B | $10.9M (Binance) | $128M | ≈2,200× |
| Bitfinex | LEO | 33% | $6.3B | $0.07M (Bitfinex) | $0.2M | ≈90,000× |
| Gate | GT | 14% | $0.88B | $0.08M (Gate) | $1.0M | ≈11,000× |
| KuCoin | KCS | 15% | $0.49B | $0.05M (KuCoin) | $1.6M | ≈9,800× |
| Bitget | BGB | 8% | $0.46B | $0.51M (Bitget) | $13.8M | ≈900× |
| HTX | TRX | <mark class="r">47%</mark> | $3.2B (<mark class="r">69% staked</mark>) | $17.6M (ten venues; HTX itself $0.38M) | $57M (ten venues) | ≈180× |
| HTX | HTX token | 5.7% | $0.37B | $0.42M (six venues; only HTX has volume) | $7.8M | ≈880× |

**How to read**

- No exchange's affiliated token could be cleared on the order book: holdings are hundreds to tens of thousands of times the depth. **The "reserve value" of an affiliated token is price times quantity, not money that can be realised** — true for every exchange, not only HTX.
- TRX is actually the one with the best order book among these (±2% $17.6M across ten venues, perpetual open interest $238M); HTX's problem is not TRX liquidity but **its share of reserves (47% + 5.7%) and the 69% staked** — Binance's BNB is 15% with the other 73% in BTC, ETH and stablecoins; Bitfinex's LEO is 33% with the other 61% in BTC.
- To judge an exchange's ability to pay under stress, mark affiliated tokens to order-book depth rather than market price, then look at hard-asset (BTC / ETH / stablecoin) coverage of liabilities. On that basis (§5 table): Binance and OKX remain ≥100%; HTX's hard-asset coverage is under half.

## 9. Reproduce

```bash
pip install curl_cffi
python3 tools/cex_reserves_verify.py --chain all                                    # all three chains
python3 tools/cex_reserves_verify.py --chain eth --ex okx --retry-failed data/cex_reserves_2026-09-04.json
python3 tools/cex_reserves_verify.py --refresh-addresses                            # re-pull official address lists
python3 tools/beacon_validators.py 0x3262f13a39efaca789ae58390441c9ed76bc658a 0xf666814c2ae92ca0e06667f80dac1eb8a97e48ae 0x5c95a672e34b3252482ed9a215f2926d2887845d 0x88a4df73aac310484c60c4c0ac4904cab938c20b   # count Beacon-chain validators by withdrawal address (§3.2 Bitstamp)
python3 tools/por_fetch.py                                                          # official PoR self-reported figures (§3.1 last column; Binance needs a manually saved page, data/por_manual.json)
```

Known pitfalls (handled in the scripts): public nodes silently truncate batched `eth_call`; Tron `eth_getBalance` excludes staked TRX, use `getaccount`; trongrid's free tier is 3 rps and silently degrades if pushed; Blockscout has no price for platform tokens, so KCS/GT/BGB are read directly on chain.

## 10. Monitoring indicators (one set, read per exchange)

The six indicators below are read the same way for every exchange, with the same trigger rules; readings are from the 2026-09-03 snapshot. "—" = not applicable to that exchange (no custody column, no native staking token, no affiliated asset).

| Indicator | Reading | Trigger | Binance | OKX | Bitget | Gate | HTX | Poloniex |
|---|---|---|---|---|---|---|---|---|
| Third-party custody share of reserves | Custody column on official PoR page | >10% | 0.9% | 2.6% | — | — | <mark class="r">19.1%</mark> | — |
| Own wallets only ÷ user liabilities | Official PoR page | <100% | 100.9% | 103.0% | ≥100% (USDT exactly 100%) | 127% | <mark class="r">84.2%</mark> | ≥100% |
| Stablecoin balance on published addresses | `--chain tron/eth` (official list) | main trading stablecoin < 1% of liabilities | USDT 1,248M (Tron) + 28.7B (ETH) | 261M + 7.75B | 242M + 569M | 75M + 372M | <mark class="r">1.9M (Tron) + 0 (ETH)</mark>, plus stUSDT 39.6M | 3.9M + 23M |
| Native-token staked share | trongrid `getaccount` | >50% | 0% | 0% | 0% | 0% | <mark class="r">69%</mark> | 0% (sTRX counted separately) |
| Single-address share of reserves | Direct read per chain | >50% | <10% | <10% | <10% | <10% | 32% (largest TRX address, ⚠ estimate) | <mark class="r">63%</mark> |
| Affiliated asset pledged for borrowing in a lending protocol | JustLend `borrowBalance` | goes from 0 to non-zero | — | — | — | — | BTCTRON collateral address: 0 (line ≈$290M) | same (issuer) |
| Main-channel withdrawal status | Each venue's `currencies` API | any prohibited | normal | normal | normal | normal | normal | normal |

---

**Source grades**

- **Primary**: direct on-chain reads; official PoR pages and GitHub lists; the FCDO sanctions list; each venue's public market API.
- **Third party**: DefiLlama, CoinGecko.
- **Media ⚠**: Protos, TRM Labs and similar reporting, used only as leads.

---

**Disclaimer**

This page is a compilation and cross-check of public data. It is not investment advice and makes no claim about any institution's solvency. All liability-side figures are self-reported by the exchanges and cannot be verified by this report.
