# A cache fallback, an API cap, and months of 9.6x-wrong data

A data aggregator I was cross-checking reported that an exchange held **4,180 BTC**. The addresses that exchange publishes held about **40,000**. The gap was not fraud, a definitional dispute, or a missing address list. It was three ordinary pieces of code doing exactly what they were written to do.

## The chain of events

**1. An upstream API tightened a limit.**

The exchange publishes its wallet addresses through a paginated endpoint. At some point it capped `per_page` at 100:

```console
$ curl -s 'https://www.bitstamp.net/api/v2/wallet_transparency/?perPage=1000&page=1'
{"code": 400, "message": "{'per_page': ['Must be greater than or equal to 1
 and less than or equal to 100.']}"}
```

**2. The adapter still asked for 1000.**

```js
const data = await get('https://.../wallet_transparency/?perPage=1000&page=' + page)
```

So the fetch threw on page 1. Every time.

**3. The config loader caught the exception and returned the last known good value.**

```js
} catch (e) {
  sdk.log(project, 'trying to fetch from cache, failed to fetch data from endpoint:', endpoint)
  return getCache(key, project)
}
```

That is the whole bug. Not the 400 — the 400 is correct behaviour by the upstream API, and an adapter that dies loudly on a 400 gets fixed the same week. The problem is that the failure was converted into a *success* carrying stale data, and the only trace was one `sdk.log` line in a system that produces a great many log lines.

The adapter kept working. It kept producing a number. The number was from an address list that had stopped being updated.

## Why the obvious fix makes it worse

The first patch anyone writes is `perPage=1000` → `perPage=100`. Here is what happens when you do only that. The pagination loop ends like this:

```js
page++
hasMorePages = !lastItem || currentLastItem.address !== lastItem.address
lastItem = currentLastItem
```

The stop condition is "the last item of this page is the same as the last item of the previous page". There is no end-of-data signal from the API, so the loop infers termination from data equality. That inference is wrong for this endpoint — page contents are not stable across calls — and it fires early.

Replaying the loop against the live endpoint:

| variant | pages read | bitcoin addresses collected |
|---|---|---|
| current code (`perPage=1000`) | 0 — throws on page 1 | falls back to stale cache |
| page size fixed only | 3 | **0** |
| page size + empty-page stop | 37 | **507** |

Replays of the "page size fixed only" variant do not stop at the same page every time — 3 pages in one run, 16 in another — because the stop condition depends on page contents that are not stable across calls. The bitcoin count was 0 in every replay: the stop point is data-dependent, the undercount is not.

The minimal fix turns a loud failure into a quiet undercount that reports zero addresses for an entire chain without erroring. It is *strictly worse* than the bug it replaces, because the bug at least left a stale value that looked implausible enough for someone to check.

There is a third landmine in the same function. When the page size is correct, page 38 returns `{"wallets": {}}`. The loop reaches for `allWallets[allWallets.length - 1].address` on an empty array and throws a `TypeError`. So the naive fix does not even reach its own bad stop condition on a longer address list — it crashes first.

The actual patch is three lines: request 100, stop when a page comes back with no wallets, and delete the `lastItem` heuristic entirely.

## What I take from it

**"Fall back to cache on error" is a silent-corruption generator unless the staleness is visible downstream.** The pattern is defensible — you would rather serve yesterday's data than nothing — but it needs an age or a freshness flag that reaches whoever consumes the number. Here, nothing distinguished "read from the live endpoint" from "read from a cache that last succeeded months ago". A consumer could not tell, and did not.

**Inferring the end of a paginated collection from data equality is a bug waiting for the data to change.** The endpoint gives no total, no cursor and no explicit terminator, so the loop guessed. The guess was "the same last element twice means we're done." That is only true for a stable, deterministically ordered collection, and nothing promised either.

**When a wrong number is discovered, the fix is not obvious and the obvious fix is not the fix.** I would have shipped the one-character change if I had not replayed the loop first.

The patch is merged: https://github.com/DefiLlama/DefiLlama-Adapters/pull/20878 — the live figure corrected from 4,180 to 40,167 two minutes after the merge.

---

*Found while building an on-chain cross-check of exchange reserve claims: https://github.com/ronfi/cex-reserves*
