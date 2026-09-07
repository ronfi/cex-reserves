# Top Exchange Reserves Check · 2026-09

> Each table heading carries its own read time. Every number can be re-read with `tools/cex_reserves_verify.py` in this repository; the output snapshot is `data/cex_reserves_2026-09-07.json`.
> Source discipline: **direct on-chain read > official PoR page > public aggregator > media**. The first three go into tables; media is used only as a lead, marked ⚠, and never tabulated.
> This page makes no judgement about any exchange's solvency; it presents verifiable facts and the differences between sources.

## 0. Summary

1. **The distribution: of the 20 exchanges, 18 hold under 20% of reserves in affiliated tokens, and only two are above 30% — the highest at 78%, the next at 32%.** Eight hold none at all; **across the twelve that do, the median is 13%** (⚠ caliber: counting the eight zeros as well, the median across all 20 is 2.5% — the two medians are not the same thing, and a citation must say which). Exchange by exchange in §4.2.
2. Among top exchanges, **HTX is the only one holding all four kinds of affiliated assets**: a platform token (HTX token), an affiliated stablecoin (USDD), self-issued wrapped coins (BTC-TRC20, HBTC), and JustLend yield receipts (stUSDT/jUSDD). Every other exchange has at most one kind (classification and the three FTX criteria in §4).
3. **HTX reports reserve ratios "all above 100%", but on the on-chain-verifiable basis: own-wallet USDT covers only 4.8% of liabilities, BTC 42%, ETH 25%; 18.1% of total reserves sit with an undisclosed "third-party custodian", and 47.5% is TRX, 69% of which is staked.** (self-reported figures are the 2026-09-01 page snapshot; on-chain figures are direct reads of 09-07)
4. Binance / OKX reserves reconcile on the ETH chain at 95–99%; Bitfinex, Gate, KuCoin and Gemini at 98–101%; all eleven reconcile on the BTC chain (difference ≤1.0%). Every exchange self-reports a reserve ratio above 100%; this report can only verify the part that is readable on chain, and each exchange's verifiable share is in §3.

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

## 2. Panorama: top 20 by on-chain reserves (DefiLlama public-address basis, read 2026-09-07 01:08 UTC)

Sample rule: **the top 20 by on-chain assets on the DefiLlama CEX board**, no discretionary additions or removals; Coinbase / Kraken / Upbit publish no addresses and are not on the board.

- Self-check entry points: the board <https://defillama.com/cexs>; per-exchange pages `https://defillama.com/cex/<slug>` (e.g. <https://defillama.com/cex/htx>, <https://defillama.com/cex/binance-cex>); the API `https://api.llama.fi/protocol/<slug>` (per-chain `currentChainTvls` and token breakdown); DefiLlama-Adapters source <https://github.com/DefiLlama/DefiLlama-Adapters/tree/main/projects> (address lists or fetch logic live there).

- "Affiliated token" = an asset issued by the exchange or its controller; the uniform red rule is **affiliated tokens >30% of reserves**.
- "1-year net flow" = the residual change in reserves after removing price effects (positive = net inflow); price baseline from Binance daily closes: BTC −28.0%, ETH −42.9%, stablecoins 0, affiliated/other ≈ −40%.
- ⚠ The Bitstamp row is the aggregator's 09-04 22:30 UTC read; this report's direct read is 39,951 BTC (§3.1).

| # | Exchange | On-chain reserves | BTC | ETH | Stablecoins | Affiliated | 1-yr net flow |
|---|---|---|---|---|---|---|---|
| 1 | Binance | $170.3B | 30% | 11% | 31% | 16%(BNB) | +15.4% |
| 2 | OKX | $30.5B | 37% | 10% | 39% | 5%(OKB) | +29.6% |
| 3 | Bitfinex | $19.4B | 61% | 3% | 3% | <mark class="r">**32%(LEO)**</mark> | +3.5% |
| 4 | Bybit | $14.7B | 31% | 13% | 29% | 4%(MNT) | -12.6% |
| 5 | Robinhood (broker) | $14.7B | 77% | 21% | 0% | 0% | -0.0% |
| 6 | Gate | $7.1B | 21% | 15% | 16% | 15%(GT) | +14.8% |
| 7 | Bitget | $6.0B | 39% | 7% | 19% | 8%(BGB) | +35.2% |
| 8 | Gemini | $5.4B | 84% | 14% | 0% | 0% | -13.8% |
| 9 | MEXC | $5.3B | 18% | 3% | 47% | 11%(MX) | +51.1% |
| 10 | Deribit | $5.1B | 77% | 11% | 11% | 0% | +30.4% |
| 11 | Bitstamp | $4.7B | 68% | 21% | 1% | 0% | +129.4% ⚠ not an inflow (see reading) |
| 12 | HTX | $4.2B | 16% | 2% | 0% | <mark class="r">**78%(HT,HTX,TRON,TRX)**</mark> | -1.2% |
| 13 | KuCoin | $3.3B | 19% | 9% | 30% | 15%(KCS) | -10.1% |
| 14 | Crypto.com | $2.5B | 74% | 8% | 9% | 1%(CRO) | -7.0% |
| 15 | HashKey | $1.7B | 65% | 25% | 5% | 0% | +32.4% |
| 16 | Poloniex | $1.6B | 49% | 40% | 1% | 1%(BTT,JST,NFT,SUN,TRX,USDD,WIN) | +45.4% ⚠ not customer inflow (see reading and §7); window only 191 days (from 02-28) |
| 17 | Bitkub | $1.5B | 65% | 14% | 3% | 0% | +34.8% |
| 18 | SwissBorg | $1.0B | 43% | 14% | 6% | 15%(BORG) | -0.8% |
| 19 | BitMEX | $0.8B | 87% | 0% | 13% | 0% | -60.4% (voluntary shutdown 2026-09-23, withdraw before wind-down) |
| 20 | OSL | $0.8B | 73% | 19% | 6% | 0% | +7.9% ⚠ window only 235 days (from 01-15) |

**How to read**

- Only two exchanges hold more than 30% of reserves in affiliated tokens: **HTX 78%, Bitfinex 32%**. LEO is the platform token iFinex issued in 2019 (not a stablecoin; supported by revenue buybacks and burns), in the same class as BNB, OKB, GT and KCS, and flagged by the same rule.
- The remaining 61% of Bitfinex is BTC.
- Bitstamp +121.3% is not an inflow: the aggregator DefiLlama-Adapters's pagination bug was fixed and its address set completed (DefiLlama-Adapters PR #20878, merged 09-04); its BTC read went from 4,180 to 40,167.
- Poloniex +61.1% is not customer inflow: between 2026-05-30 and 06-04, 71,993 stETH, 806M sUSDS and 1,723 WBTC entered Poloniex 9 (the address holding 63% of its reserves) through two Poloniex-published addresses. The stETH leg traces back to HTX address `0x18709E89…` (attribution verified in §7); the 1,723 WBTC and 200M of the sUSDS trace to the same address; the other 606M sUSDS comes from an unlabelled hub that mints sUSDS itself, and its HTX origin could not be established on chain. Hop by hop in §7.
- The rest of HTX is 18% BTC (half of it the BTC-TRC20 of §7.2) and 2% ETH; there are no stablecoins on the aggregator's address set. Gemini, Bitstamp and Robinhood are also at 0% stablecoins, which is not a discrepancy in itself; the read of own-wallet USDT on HTX's official PoR list is in §6.2.

## 3. Direct on-chain reconciliation of published addresses (primary evidence)

§2 is the aggregator's basis; this section is **this report reading the chains itself**: take each exchange's published addresses (official PoR list or DefiLlama-Adapters source, see `tools/cex_addresses.json`), read BTC / all ETH assets / Tron per address, then reconcile against the aggregator. **Tables are generated by `tools/make_tables.py` from `data/cex_reserves_2026-09-07.json`**; every address's read and failure record is in that file.

### 3.1 BTC chain (mempool.space direct read vs aggregator; difference ≤1% green, >5% red)

| Exchange | Addresses (read/total) | Direct BTC | Aggregator BTC | Diff | PoR BTC: users / wallets (snapshot) | Direct − PoR wallets |
|---|---|---|---|---|---|---|
| Binance | 61/61 | 639,647 | 639,647 | <span class="ok">+0.0%</span> | 656,644 / 658,293(08-01) | -2.8% |
| Bitfinex | 3/3 | 147,973 | 147,980 | <span class="ok">-0.0%</span> | — | — |
| Bybit | 25/25 | 57,605 | 57,612 | <span class="ok">-0.0%</span> | 56,438 / 59,064(07-23) | -2.5% |
| Gate | 13/13 | 18,857 | 18,831 | <span class="ok">+0.1%</span> | 22,436 / 27,550(08-19) | <mark class="r">-31.6%</mark>(the 13-address DefiLlama-Adapters list is not every wallet on the page (Gate publishes no BTC addresses)) |
| Bitget | 19/19 | 29,461 | 29,473 | <span class="ok">-0.0%</span> | 26,811 / 35,837(08-20) | <mark class="r">-17.8%</mark>(the 19-address adapter list is not every wallet on the page; page wallets include 535 BTC on BSC/Lightning etc.) |
| MEXC | 34/34 | 11,691 | 11,692 | <span class="ok">-0.0%</span> | 4,282 / 12,313(08-09) | <mark class="r">-5.0%</mark> |
| Gemini | 4/4 | 56,437 | 56,439 | <span class="ok">-0.0%</span> | — | — |
| Deribit | 17/17 | 49,546 | 49,550 | <span class="ok">-0.0%</span> | — | — |
| HTX | 11/11 | 8,292 | 8,213 | <span class="ok">+1.0%</span> | 19,498 / 20,252(09-01) | <mark class="r">-59.1%</mark>(reported wallets 20,252 = exchange 18,563 + custody 1,689; the exchange figure includes BTC-TRC20, 10,331 on chain 09-07, leaving ~8,232 against the 8,292 read here, +0.7%) |
| Crypto.com | 8/8 | 22,873 | 22,864 | <span class="ok">+0.0%</span> | — | — |
| Bitstamp | 507/507 | 39,763 | 40,114 | <span class="ok">-0.9%</span> | — | — |

**How to read**

- **All eleven reconcile** (difference ≤1.0%); the aggregator's BTC figures can be cited directly.
- The HTX row is the DefiLlama-Adapters's 11-address list; its official PoR list has 7 addresses holding 8,073 BTC on chain (§6.2).
- The Gate list once contained 3 strings starting with `3P` that returned 404 on both BTC explorers; decoded, they are not Bitcoin addresses (35 characters, checksum fails) but Waves-chain addresses from the `waves` section of the DefiLlama-Adapters (Waves mainnet addresses happen to start with 3P), mis-sorted into BTC by prefix when this report extracted them. They are removed, and the script now validates addresses.
- The last two columns: each exchange's self-reported BTC from its official PoR page (user liabilities / exchange wallets incl. custody; fetched by `tools/por_fetch.py`, Binance and Bybit entered manually), and the direct read's difference from the reported wallets (percent). Differences over 5% are red with the reason: they come from snapshot dates, address sets (the DefiLlama-Adapters address list is not every wallet on the page) and caliber (HTX counts BTC-TRC20 and custody as wallets), and are not a reserve-check criterion. OKX (134,399 / 148,552, 08-11) and KuCoin (7,441 / 7,985, 08-31) self-report BTC but publish no BTC addresses, so they are not in the table. Bitfinex, Gemini and Bitstamp have no Merkle PoR page and report no per-coin figures; Deribit stopped publishing PoR on 2026-09-01 (90% of client assets moved to Coinbase custody); Crypto.com has a page but its figures are script-rendered and no snapshot has been taken yet.

### 3.2 ETH chain (Blockscout all-asset direct read vs aggregator; the "aggregator-caliber" column excludes USDD/HBTC/aEthUSDT; coverage 95–105% green, <90% or >110% red)

| Exchange | Addresses | All-asset read | Aggregator-caliber read | Aggregator | Coverage | Failed | Direct native ETH | PoR ETH: users / wallets (snapshot) | Direct native − PoR wallets |
|---|---|---|---|---|---|---|---|---|---|
| Binance | 37 + lock 2 | $69.31B | $69.30B | $69.92B | <span class="ok">99%</span> | 0 | 3,244,790 | ? / 3,991,221(08-01) | -19% |
| OKX | 323 | $13.21B | $13.20B | $13.86B | <span class="ok">95%</span> | 0 | 1,005,248 | 1,725,703 / 1,749,426(2026-08) | -43% |
| Bitfinex | 9 | $7.25B | $7.25B | $7.21B | <span class="ok">101%</span> | 0 | 216,646 | — | — |
| Gate | 91 | $3.17B | $3.17B | $3.18B | <span class="ok">100%</span> | 0 | 172,274 | 375,430 / 458,203(08-19) | -62% |
| Bitget | 80 | $1.58B | $1.58B | $1.63B | <span class="ok">97%</span> | 0 | 121,323 | 123,688 / 190,090(08-20) | -36% |
| Gemini | 5 | $0.82B | $0.82B | $0.84B | <span class="ok">98%</span> | 0 | 288,687 | — | — |
| HTX | 57 | $0.22B | $0.14B | $0.13B | <span class="ok">105%</span> | 0 | 11,118 | 114,984 / 116,757(09-01) | -90% |
| KuCoin | 96 | $1.63B | $1.63B | $1.64B | <span class="ok">99%</span> | 0 | 90,693 | 101,664 / 118,497(08-31) | -23% |
| Bitstamp | 64 | $0.57B | $0.57B | $1.16B | <mark class="n">49%*</mark> | 0 | 168,938 | — | — |

**How to read**

- **Eight exchanges at 95–101%**; the aggregator can be cited.
- HTX's all-asset read of $0.22B exceeds the aggregator's $0.12B; the gap is exactly USDD $45M + HBTC $42M. The aggregator excludes exchange-issued or affiliated assets (§1 rules); on the same caliber it is 108%.
- \* Bitstamp 51%: a caliber difference, not an address difference. DefiLlama counts all Beacon-chain staked ETH whose withdrawal credentials point to Bitstamp addresses (≈233k ETH, 8,011 validators) as Bitstamp reserves; this report does not, because staked ETH sits on no published address's balance, and two of the four withdrawal addresses are not on Bitstamp's published list, so the attribution rests on the aggregator's own address table alone. Adding that part back, the two sides reconcile. Independent check: `tools/beacon_validators.py` (§9).
- The Binance row includes 2 pegged-token lock addresses ($12.3B), not customer assets. "Pegged-token lock" means the native collateral Binance locks on Ethereum mainnet for the Binance-Peg tokens it issues on BNB Chain (BSC versions of USDT, USDC, ETH, etc.); the liability side is the holders of those pegged tokens, not exchange customers. The addresses come from Binance's lockinfo endpoint and are not on its PoR list; a proposal to split them out has been filed with the aggregator (DefiLlama-Adapters PR #20885, pending maintainers).
- "Failed addresses" are all 0 (one OKX address cleared after a retry).
- The last column is each exchange's self-reported ETH (users / wallets, snapshot dates vary). Its caliber is **ETH across all chains** (L2s, staking receipts and custody included), not the same as this table's Ethereum-mainnet dollar read, so it is shown for reference only and no difference is computed.
- The added "Direct native ETH" column counts only native ETH on Ethereum-mainnet addresses (no stETH-type receipts, no L2), script `tools/eth_native_units.py`, read 09-05; the PoR ETH wallet figure is **all-chain** (L2s, staking receipts and custody included), so "Direct native − PoR wallets" is generally negative, shown for reference only and not judged by the §3.1 red rule. Example: of HTX's reported 116,757 wallet ETH (09-01), 87,525 is custody and 29,158 stETH, with only 1,504 native mainnet ETH (its GitHub snapshot CSV), the same order as the 11,118 read directly; Binance −18% and OKX −42% mostly reflect multi-chain pages and differing address sets.

### 3.3 Tron chain (trongrid `getaccount` with four staking buckets + direct USDT-TRC20 read)

| Exchange | Addresses | TRX available | TRX staked | USDT-TRC20 | PoR TRX: users / wallets | Direct TRX − PoR wallets | PoR USDT (all chains): users / wallets |
|---|---|---|---|---|---|---|---|
| Binance | 25 | 2,283M | 0M | 1,253.2M | — | — | — |
| OKX | 23 | 134M | 517M | 265.0M | — | — | 8,118M / 8,637M(2026-08) |
| Bitfinex | 2 | 28M | 42M | 119.2M | — | — | — |
| Gate | 11 | 13M | 84M | 80.1M | 58M / 179M(08-19) | <mark class="r">-45.6%</mark>(the 11-address DefiLlama-Adapters list is not every wallet on the page (Gate publishes no TRX addresses)) | 660M / 721M(08-19) |
| Bitget | 29 | 5M | 0M | 247.0M | — | — | 1,454M / 1,456M(08-20) |
| HTX | 18 | 3,037M | 6,733M | 0.0M | 8,620M / 9,384M(09-01) | +4.1% | 872M / 588M(09-01) |
| KuCoin | 24 | 15M | 62M | 104.5M | — | — | 955M / 1,059M(08-31) |

**How to read**

- **The aggregator cannot be cited here.** It misses USDT-TRC20 (Bitget's published addresses hold 247M, the aggregator records 0), and its `eth_getBalance` read excludes staked TRX.
- Tron's "freeze" is its official term for staking TRX with the network in exchange for bandwidth, energy and votes: ownership is unchanged, unstaking can be started at any time and lands 14 days later; it is neither loan collateral nor a platform or judicial freeze. This report says "staked" throughout. Staked TRX can be in four places: V1 stake, V2 self-held stake, **stake delegated to other addresses** (the TRX still belongs to the address), and the unstaking queue; the "TRX staked" column counts all four. OKX's 517M and Poloniex's 24M are delegated stake, invisible if you only read `balance + frozenV2` (§7.1).
- HTX's 18 Tron addresses in the table are the DefiLlama-Adapters's TRX cold wallets; holding no USDT there is normal. **HTX's official PoR has 5 separate USDT-TRC20 addresses**: 13.24M in the 08-01 snapshot, <mark class="r">1.91M</mark> on chain on 09-07 (below 1% of the user USDT liability, the §10 rule; the 11.33M on `TK86…` has been emptied); the single USDT-ERC20 address went 1.05M → 0. The rest of the 926M user USDT liability sits in "ThirdParty" (§6.2).
- The last two columns are each exchange's self-reported TRX and USDT (users / wallets); USDT is the **all-chain total** (ERC20 + TRC20 + others) while this table's USDT-TRC20 is one chain, so no difference is computed. HTX's reported TRX wallets of 9,384M (09-01) are in the same range as this table's 9,770M across 18 addresses (available + staked, 09-07); of its reported 588M USDT wallets, 547M sit in "ThirdParty" (93%, §6.2).
- "Direct TRX − PoR wallets": direct TRX (available + staked) and the reported TRX wallet are the same chain and caliber, so they compare directly; over 5% is red with the reason, as in §3.1. Gate −92% is an address-set difference (the 11-address DefiLlama-Adapters list; Gate publishes no TRX addresses); HTX +3.4%. No difference is computed for USDT because the reported figure is all-chain.

## 4. Affiliated tokens as a share of reserves: FTX's three structural preconditions, exchange by exchange

### 4.1 What FTX's structural preconditions were (⚠ public reporting, used only as the source of the criteria)

FTX's balance-sheet structure before its November 2022 collapse is where this chapter's criteria come from. Note: FTX the exchange never published its own reserve composition; the criteria here come from the balance sheet of its affiliated market maker Alameda, which is not the same basis as the exchange reserve shares in §2 and cannot be compared with them directly. Three points:

- **Its own token was the bulk of assets**: on 2022-11-02 CoinDesk published the balance sheet of Alameda, FTX's affiliated market maker: of $14.6B in assets, $3.66B was FTX's platform token FTT and another $2.16B was "FTT collateral"; FTT-related items exceeded a third of assets (<https://www.coindesk.com/business/2022/11/02/divisions-in-sam-bankman-frieds-crypto-empire-blur-on-his-trading-titan-alamedas-balance-sheet>).
- **Its own token had no order book**: most of the FTT float sat with FTX and Alameda themselves; market cap was list price times quantity, not money that could be realised. On 11-06 Binance announced it would sell its FTT, and FTT lost 80% over the next three days.
- **The liability side was opaque**: customer deposits had been diverted to Alameda, and outsiders could not see how liabilities matched assets; withdrawals were halted on 11-08 and bankruptcy filed on 11-11.

The criterion: **what is fatal is not "holding your own token", it is all three at once** — ① the own token is the bulk of reserves; ② the own token has no order book; ③ the liability side is opaque. Below, every exchange is checked against the same rules.

### 4.2 By exchange: affiliated tokens as a share of reserves (data as in §2; red rule as in §2: affiliated >30% of reserves)

"Hard assets" = BTC + ETH + stablecoins; whatever the two columns leave short of 100% is other coins (SOL, XRP, etc.).

| Exchange | Affiliated token | Share of reserves | Hard assets |
|---|---|---|---|
| HTX | TRX + HTX token | <mark class="r">**78%**</mark> | 18% |
| Bitfinex | LEO | <mark class="r">**32%**</mark> | 68% |
| Binance | BNB | 16% | 72% |
| KuCoin | KCS | 15% | 59% |
| SwissBorg | BORG | 15% | 63% |
| Gate | GT | 15% | 53% |
| MEXC | MX | 11% | 68% |
| Bitget | BGB | 8% | 66% |
| OKX | OKB | 5% | 86% |
| Bybit | MNT | 4% | 74% |
| Poloniex | Affiliated-group tokens | 1% | 90% |
| Crypto.com | CRO | 1% | 90% |
| Robinhood, Gemini, Deribit, Bitstamp, HashKey, Bitkub, BitMEX, OSL | — | 0% | 79–100% |

- Two exchanges are above 30%: HTX 78%, Bitfinex 32%. The difference is in hard assets: Bitfinex holds 68% hard assets, twice its LEO; HTX holds 18%, with affiliated tokens more than four times that. Whether affiliated tokens exceed hard assets is the basis of criterion ① in §4.4.
- The table above is on the aggregator's basis (published addresses only, self-issued/affiliated assets excluded). On HTX's own PoR snapshot basis (2026-09-01; §5, §6.2): TRX is 47.5%, HTX token 6.1%, and 51% of the BTC line is the Poloniex-issued BTC-TRC20 (§7).

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
| Issuer / mechanism | Issued 2022-05 by TRON DAO Reserve (⚠ public reporting describes it as under the same controller as HTX); launched as an algorithmic coin, restyled "over-collateralised" after the 2022-06 depeg, and in 2025 changed to minting against locked TRX/USDT (⚠ history from public reporting) |
| Size and holdings (primary) | Supply $1.51B, mostly on Tron (<https://defillama.com/stablecoin/usdd>); HTX counts it in its "USDs" stablecoin reserves, 125M in own wallets (PoR page USDs breakdown) |
| Verifiability | Balances verifiable; **the collateral is TRX**, the same asset as the bulk of the reserves |

**③ Self-issued wrapped coins**

| Item | Detail |
|---|---|
| Assets | BTC-TRC20 (BTCTRON), HBTC |
| Issuer / mechanism | BTCTRON: issued by Poloniex on Tron in 2020, claims 1:1 redemption, has never disclosed a collateral address (<https://tronscan.org/#/token20/TN3W4H6rK2ce4vX9YnFQHwKENnHjoxb3m9>); HBTC: wrapped BTC issued by Huobi on Ethereum in 2020, discontinued after the rebrand to HTX (<https://etherscan.io/token/0x0316EB71485b0Ab14103307bf65a021042c6d380>) |
| Size and holdings (primary) | BTCTRON supply 17,545, HTX holds 10,331 (direct read 2026-09-07), 51% of its PoR BTC line; HBTC supply only 969.49, HTX addresses hold ≈540 (56%) |
| Verifiability | Balances verifiable; **we could not locate BTCTRON collateral in the published addresses at either end (§7.2; on-chain search cannot rule it out); the HBTC issuer holds more than half of it itself** |

**④ Yield / lending receipts**

| Item | Detail |
|---|---|
| Assets | stUSDT, jUSDT, jUSDD, sTRX (JustLend); stETH (Lido); WBETH (Binance); aEthUSDT (Aave); sUSDS (Sky) |
| Issuer / mechanism | Shares received for depositing the underlying into a protocol, booked in reserves as the underlying (stUSDT as USDT, stETH as ETH) |
| Size and holdings (primary) | 73% of HTX's own-wallet USDT is stUSDT (39.55M; ⚠ that composition is from the 08-01 per-chain snapshot, HTX has not published the 09-01 per-chain data, §6.2); Poloniex snapshot sUSDS 912.6M, stETH 247.8k (§7); Binance WBETH $8.4B; the aEthUSDT pool on chain 09-03: total supply ≈$2.95B, cash in pool $236M, utilisation 92% (<https://etherscan.io/token/0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a>) |
| Verifiability | Balances verifiable; **instant redemption depends on the cash in the protocol**, and every depositor stands in the same queue; the underlying of JustLend receipts (<https://tronscan.org/#/token20/TThzxNRLrW2Brp9DcTQU8i4Wd9udCWEdZ3>) is itself inside JustLend, and JustLend accepts BTCTRON as collateral (§7.2) |

- Only HTX has all four kinds: platform token + affiliated stablecoin + self-issued wrapped coins + yield receipts from an affiliated protocol.
- The aggregator's basis excludes ② and ③, which is exactly the gap between the "aggregator-caliber" and "all-asset" columns for HTX's ETH chain in §3.2.
- Of the four kinds, only the non-affiliated part of ④ (stETH, WBETH, sUSDS, aEthUSDT) is "someone else's credit"; everything else is "own credit".

### 4.4 The three criteria, exchange by exchange (exchanges with affiliated ≥10%, plus those publishing per-coin liabilities)

| Exchange | ① Affiliated = bulk of reserves | ② Holding ÷ major-venue 30-day avg volume (days to sell all, §8) | ③ Liability side (§5) |
|---|---|---|---|
| HTX | <mark class="r">**Yes** (78% vs hard assets 18%)</mark> | TRX ≈45 days, HTX token ≈13 days | Publishes per-coin liabilities; **19% of reserves with a custodian not disclosed on the page, own-wallet USDT covers 5.8% of liabilities** (§6.2) |
| Bitfinex | No (32% vs 68%) | LEO ≈26,700 days | No PoR page, liabilities unpublished |
| KuCoin | No (15% vs 59%) | KCS ≈96 days | Ratio only, 110% |
| SwissBorg | No (15% vs 63%) | Not measured | No PoR page |
| Binance | No (16% vs 72%) | BNB ≈177 days | Publishes per-coin liabilities; own wallets ÷ liabilities 100.9% |
| Gate | No (15% vs 53%) | GT ≈1,430 days | Ratio only, 127% |
| MEXC | No (11% vs 68%) | Not measured | Ratio only, 141% |
| OKX | No (5% vs 86%) | Not measured | Publishes per-coin liabilities, 103.0% |

**How to read**

- ① holds for one exchange only.
- ② on its own does not rank danger: days-to-sell runs from a couple of weeks to tens of thousands of days and must be read with ①; the higher the affiliated share and the thinner the volume, the more the reserves shrink once marked to tradable volume.
- ③ Only Binance, OKX and HTX publish per-coin liabilities; the rest either give a single ratio or have no PoR page.
- No exchange in the top 20 meets all three at once; the closest is HTX: ① holds, ② about 45 days to sell (TRX is the most actively traded of these tokens), ③ liabilities are published but a fifth of reserves sit with a custodian not disclosed on the page. The differences from FTX: TRX has a market-wide order book and FTT did not; HTX publishes a liability sheet and FTX did not. The similarity: reserve value is a function of the price of its own family of tokens.

## 5. Official PoR side by side (each exchange's page, snapshot dates vary — see the first column; red = third-party custody >10% of reserves or own wallets ÷ liabilities <100%, the §10 trigger rules)

| Exchange | User liabilities | Reported reserves | Third-party custody share | **Own wallets ÷ liabilities** |
|---|---|---|---|---|
| Binance | $127.9B | $130.3B | 0.9% | 100.9% |
| OKX (21 assets) | $30.8B | $32.6B | 2.6% | 103.0% |
| HTX (09-01) | $6.03B | $6.37B | <mark class="r">**18.1%** (custodian undisclosed)</mark> | <mark class="r">**86.5%**</mark> |
| Gate | — | 127% | no custody column | — |
| Bitget | — | 120% (USDT 100%, zero surplus) | no custody column | — |
| KuCoin | — | 110% | no custody column | — |
| MEXC | — | 141% | no custody column | — |
| Kraken | — | ratio only | — | — |

## 6. Discrepancies with self-reported figures (by exchange)

The same reading is applied to every exchange. This section lists the differences between what this report reads and what each exchange reports, each with its verification method; it sets no thresholds, so it uses no colour, only bold for the item.

### 6.1 Binance / Poloniex

| Exchange | Discrepancy | Reading | How to verify |
|---|---|---|---|
| Binance | The aggregator counts pegged-token collateral as "reserves" | **$12.3B of DefiLlama's $69.1B comes from 2 lockinfo addresses** (USDT 9.18B, USDC 1.58B, ETH 455k), not customer assets; the 37 PoR addresses alone hold $56.4B | `eth_lock` in `tools/cex_addresses.json`; `--chain eth --ex binance-cex` |
| Poloniex | Reserve composition and concentration | **94% of "USDT" is sUSDS, 98% of "ETH" is stETH, one address holds 63% of reserves**; published TRX addresses −18% in a month (§7.1 per address) | §7 |

### 6.2 HTX


| # | Discrepancy | Reading | How to verify |
|---|---|---|---|
| 1 | **Own-wallet USDT covers only 4.8% of liabilities; 93% of USDT reserves sit in third-party custody** | 09-01 page: liabilities 872.3M; own wallets **41.46M** (÷ liabilities = 4.8%); custody 546.87M (93% of USDT reserves). ⚠ The per-chain composition of own wallets (08-01: USDT-TRC20 13.24M + USDT-ERC20 1.05M + stUSDT 39.55M, i.e. 73% JustLend receipts) exists only in the GitHub CSV, which has no 09-01 version yet. The 5 official USDT-TRC20 addresses on chain 09-07: **1.91M** | HTX PoR page "USDs" breakdown; GitHub snapshot CSV; `--chain tron --ex htx` (`tron_por` item) |
| 2 | **18.1% of reserves in third-party custody whose custodian is not disclosed on the page** | Category added 2026-06-01; at 09-01 it holds USDT 546.9M, USDC 239.4M, ETH 87,543, BTC 1,689, USDD 6.9M, U 17.9M, SOL 1,833 and 301.8bn HTX; Binance 0.9% and OKX 2.6% on the same basis | HTX PoR page "Custodial Wallets" column |
| 3 | **51% of BTC reserves is Poloniex-issued BTC-TRC20, with no corresponding collateral found in the published addresses or the PoR page (on-chain search cannot rule it out)** | 09-01 reported BTC 20,252 = exchange wallets 18,563 + custody 1,689; BTC-TRC20 on chain 09-07 is **10,331 = 51% of reported reserves**; the 11 published addresses read 8,292 native = **42.5%** of the 19,498 user liability | `--chain btc,tron --ex htx`; BTC-TRC20 in §7.2 |
| 4 | **75.0% of ETH reserves in custody, 25.0% verifiable on chain** | 09-01 page: users 114,984 / HTX 116,757 / exchange wallets 29,213 / custody 87,543; the 11 PoR addresses on chain 09-07 read **$68.5M** (native ETH only 84.7, the rest stETH-type receipts) | `--chain eth --ex htx` (`eth_por` item) |
| 5 | **TRX is 47% of reserves, 69% staked, and the whole market's order book cannot absorb 1% of it** | 18 addresses hold 9.77B TRX = 10.3% of supply (3.04B available + 6.73B staked, 69% staked, read 09-07); the 09-01 user TRX liability is 8.62B ⇒ **35%** payable at once; ±2% spot depth across ten venues $17.6M in total, HTX holding $3.2B | trongrid `getaccount`; each venue's depth API |
| 6 | **The HTX platform token is 6.1% of reserves; the self-reported exchange wallets equal 23.2% of its supply, and it trades only on HTX** | Tron mainnet totalSupply **999.99 trillion** (contract read 2026-09-07); the 09-01 page reports **231.76 trillion in exchange wallets = 23.2% of supply**, plus 301.8bn in custody — consistent with the "about 23% self-held" figure, and it confirms that last period's "18 addresses hold 2.31 trillion" was an order-of-magnitude slip (2.31/1000 = 0.23%, off by 100×), now withdrawn. ⚠ The 23.2% is **self-reported**; the holding addresses are still not in this report's TRX cold-wallet list and the per-address on-chain check is not done. Not listed on Binance/OKX, daily volume on the five listing venues $0–50k; no perpetuals on nine venues | Tron JSON-RPC; each venue's market API |
| 7 | **95,200 BTC-TRC20 redeemed in 2024-09/10, yet HTX's real BTC fell rather than rose** | HTX monthly snapshots 09-01 → 11-01: BTC-TRC20 −8,522, native BTC −4,762, total BTC 34,611 → 21,327 (−38%); that month's PoR still reported a ratio >100% | CSVs in each commit of HTX's GitHub `huobiapi/Tool-Node.js-VerifyAddress` |
| 8 | Page is internally consistent, but less than half is verifiable — and this period one cross-source is missing | The 09-01 page reports BTC / ETH ratios of 104% / 102%; the share provably "that coin" on chain is **42.5% / 25.0%**. ⚠ **The page-vs-GitHub cell-by-cell check cannot be done this period**: `huobi_por.csv` still carries the 08-01 snapshot (HTX pushes it about 11 days after each snapshot — the 08-01 file landed on 08-12), so the 09-01 file is expected around 09-12; last period's four figures did match cell by cell | §3 and §5 of this report |

**Regulatory status (public record; not a reserve-check finding)**: UK FCDO listed Huobi Global S.A. (alias "HTX (formerly Huobi)") on 2026-05-26, updated 07-07; the EU followed in July, effective 08-23; OFAC has not acted. Source: FCDO sanctions list CSV (primary).

**Control group read with the same scripts on the same day**

- **Binance**: 61 BTC addresses, 640,647 BTC on chain (0 failures); 37 ETH addresses $56.4B; USDT-TRC20 897M.
- **OKX**: 323 ETH addresses $12.9B, 95% of the aggregator (0 failures); USDT-TRC20 273M.

## 7. Poloniex and BTC-TRC20 (BTCTRON): the Poloniex-linked part of HTX reserves

**Poloniex** (⚠ public reporting: acquired from Circle in 2019 by an investment group associated with Justin Sun; PoR address list published on GitHub `poloniex/tools-nodejs-address-verify`, same snapshot block height as HTX):

| Item | Reading |
|---|---|
| Nominal reserves (08-01 snapshot) | $2.73B |
| Composition of the $968M "USDT" reserve | **94% is sUSDS** (Sky savings shares, not USDT) |
| Composition of the 252k "ETH" reserve | **98% is stETH**, native ETH 1,142 |
| Single-address concentration | **[`0x176F3DAb…0132`](https://etherscan.io/address/0x176F3DAb24a159341c0509bB36B833E7fdd0a132) alone holds sUSDS $1.0B + stETH 243k + WBTC 1,690 ≈ $1.72B = 63% of reserves** |
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
| Supply and holders | 17,545; **[HTX 6](https://tronscan.org/#/address/TDToUxX8sH4z6moQpK3ZLAN24eupu2ivA4) holds 10,304 (58.7%) + [JustLend jBTC market](https://tronscan.org/#/contract/TLeEu311Cbw63BcmMHDgDLu7fnk9fqGcqT) 6,577 (37.5%) = 96%**; Poloniex itself holds 28 |
| Mint history | Minted 114,000 / redeemed 96,090 / blacklist-burned 364 (closes); **the 89,000 minted in 2022 went straight into JustLend the same day, not to user withdrawals** |
| Collateral | All 12,617 BTC in Poloniex's PoR already correspond to its own 12,603 user liability; **no line is marked as BTCTRON reserve; the 16 BTC addresses carry no signature**; when 95,200 were redeemed in 2024-09/10, none of Poloniex's 15 cold addresses showed an outflow ≥1,000 BTC and HTX's native BTC did not rise |
| 2022-08-21 | **The day 60,000 were minted, the two deposit addresses borrowed 400M + 600M USDC from JustLend jUSDC and sent it to a Poloniex signing address**; 95% of the jUSDC pool was supplied by hubs affiliated with the borrower; repaid 2023-07 |
| Current credit line | The JustLend oracle prices BTCTRON at full real-BTC price ($76.8k), collateral factor 0.75; **one address has 5,000 registered as collateral, borrow 0, borrowable ≈$290M; jUSDT pool cash $68M**; another address borrows $16.2M jUSDT against 200 + sTRX |

The above records what we could **not find** on Poloniex\'s published addresses and PoR page: no asset marked as BTCTRON reserve. Collateral may exist in undisclosed addresses; on-chain search cannot rule that out.

## 8. Realisability of affiliated tokens: reserve holdings ÷ 30-day average daily volume (measured 2026-09-07; red = affiliated share >30% or staked share >50%, the §2/§10 rules)

In §2 every exchange's "affiliated token" enters reserves at market price. This section asks the same question of each: **if it had to be sold, how much can the market absorb per day?** Uniform reading: the reserve holding of the token divided by the **average daily volume over the last 30 complete days** (single-day volume swings widely; the 30-day average is steadier), giving the days needed to sell it all at that pace. Volume is given on two bases: **major venues** = the spot pair's daily klines summed across whichever of Binance, OKX, Bybit, KuCoin, Gate, Bitget, Kraken, HTX, MEXC and Bitfinex list the pair (primary; venue count in the table); **market-wide** = the token's volume across all listed venues as recorded by CoinGecko (⚠ third party, venues not individually checked). Days are computed on the major-venue basis; the market-wide figure is reference only, because its bulk usually comes from venues outside the major ten (see reading). ±2% depth (dollar amount fillable at once) is listed for reference. Script `tools/affiliated_liquidity.py`, readings in `data/affiliated_liquidity_2026-09-07.json`; holdings follow the §2 reads of 09-07 (reserves × affiliated share); HTX's TRX is this report's direct on-chain read, the HTX token carries last week's figure marked ⚠.

| Exchange | Token | Share | Reserve holding | Major-venue 30-day avg daily volume (venues) | CoinGecko market-wide 30-day avg (⚠) | ±2% depth (major venues) | Holding ÷ major-venue 30-day avg (days to sell all) |
|---|---|---|---|---|---|---|---|
| Binance | BNB | 16% | $27.1B | $152.6M (8 venues) | $927.0M | $21.1M | ≈177 days |
| Bitfinex | LEO | <mark class="r">32%</mark> | $6.2B | $0.2M (2 venues) | $0.3M | $0.45M | ≈26,700 days |
| Gate | GT | 15% | $1.07B | $0.7M (1 venue) | $1.9M | $0.10M | ≈1,430 days |
| KuCoin | KCS | 15% | $0.50B | $5.2M (2 venues) | $12.8M | $0.05M | ≈96 days |
| Bitget | BGB | 8% | $0.46B | $8.8M (2 venues) | $9.5M | $0.45M | ≈52 days |
| HTX | TRX | <mark class="r">47.5%</mark> (self-reported basis) | $3.27B (direct read of 18 addresses: 9.77B TRX × $0.335; <mark class="r">69% staked</mark>) | $72.4M (10 venues; HTX itself $2.6M) | $394.9M | $16.9M (ten venues) | ≈45 days |
| HTX | HTX token | 6.1% (self-reported basis) | $0.39B (09-01 self-report 232.06 trillion × $1.68e-6) | $28.2M (6 venues; only HTX has volume) | $31.5M | $0.42M (six venues) | ≈14 days |

**How to read**

- Days-to-sell is misleading on its own and must be read with the share: Binance's BNB would take about 177 days, and BNB is only 16% of reserves with 72% in hard assets, which is not a problem; Bitfinex's LEO is 33% of reserves and would take about 26,700 days (about 73 years, the same on both bases), and only when both hold is realisability a problem. **The "reserve value" of an affiliated token is price times quantity, not money that can be realised** — true for every exchange.
- Why the market-wide basis is reference only: of CoinGecko's TRX volume, the ten major venues account for 16%; the largest contributors are FameEX (12%), WhiteBIT (7%) and Phemex (6.5%), with Binance at only 7%. Of BNB's market-wide volume, major venues account for 27%, Binance 19%, the rest from P2B, CoinUp, BTCC, XT and similar. In both cases the bulk of the market-wide figure sits on venues this report does not check individually. TRX takes about 45 days at the major-venue 30-day average (about 8 on the market-wide basis); HTX's realisability issue is not TRX volume but **its share of reserves (47% + 5.7%) and the 69% staked**. Bitfinex's LEO is 32% with the other 61% in BTC; Binance's BNB is 16% with the other 72% in BTC, ETH and stablecoins.
- To judge an exchange's ability to pay under stress, mark affiliated tokens to tradable volume rather than market price, then look at hard-asset (BTC / ETH / stablecoin) coverage of liabilities. On that basis (§5 table): Binance and OKX remain ≥100%; HTX's hard-asset coverage is under half.

## 9. Reproduce

```bash
pip install curl_cffi
python3 tools/cex_reserves_verify.py --chain all                                    # all three chains
python3 tools/cex_reserves_verify.py --chain eth --ex okx --retry-failed data/cex_reserves_2026-09-07.json
python3 tools/cex_reserves_verify.py --refresh-addresses                            # re-pull official address lists
python3 tools/beacon_validators.py 0x3262f13a39efaca789ae58390441c9ed76bc658a 0xf666814c2ae92ca0e06667f80dac1eb8a97e48ae 0x5c95a672e34b3252482ed9a215f2926d2887845d 0x88a4df73aac310484c60c4c0ac4904cab938c20b   # count Beacon-chain validators by withdrawal address (§3.2 Bitstamp)
python3 tools/por_fetch.py                                                          # official PoR self-reported figures (§3.1 last column; Binance needs a manually saved page, data/por_manual.json)
```

Known pitfalls (handled in the scripts): public nodes silently truncate batched `eth_call`; Tron `eth_getBalance` excludes staked TRX, use `getaccount`; trongrid's free tier is 3 rps and silently degrades if pushed; Blockscout has no price for platform tokens, so KCS/GT/BGB are read directly on chain.

## 10. Monitoring indicators (one set, read per exchange)

The six indicators below are read the same way for every exchange, with the same trigger rules; readings are from the 2026-09-03 snapshot. "—" = not applicable to that exchange (no custody column, no native staking token, no affiliated asset).

| Indicator | Reading | Trigger | Binance | OKX | Bitget | Gate | HTX | Poloniex |
|---|---|---|---|---|---|---|---|---|
| Third-party custody share of reserves | Custody column on official PoR page | >10% | 0.9% | 2.6% | — | — | <mark class="r">18.1%</mark> | — |
| Own wallets only ÷ user liabilities | Official PoR page | <100% | 100.9% | 103.0% | ≥100% (USDT exactly 100%) | 127% | <mark class="r">86.5%</mark> | ≥100% |
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

This page is a compilation and cross-check of public data. It is not investment advice and makes no claim about any institution's solvency. All liability-side figures are self-reported by the exchanges and cannot be verified by this report. Every statement here is limited to publicly verifiable data; not finding an asset on the published addresses does not mean the asset does not exist.
