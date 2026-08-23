<div align="center">

# CRYPTOS

### The whole HyperLiquid picture, on one screen.

Open interest, funding, smart-money positioning, AI forecasts, macro regime and event risk —
across every live HyperLiquid market: crypto, plus tokenised stocks, metals, energy and FX.

**[cryptos.broker](https://cryptos.broker)**

[![live markets](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcryptos.broker%2Fapi%2Fmarket%2Fglobal&query=%24.data.assets_count&label=live%20markets&color=00d4aa&style=flat-square)](https://cryptos.broker/api/market/global)
[![forecasts scored](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcryptos.broker%2Fapi%2Fkronos%2Faccuracy&query=%24.data.overall.n_total&label=forecasts%20scored&color=7ab8ff&style=flat-square)](https://cryptos.broker/api/kronos/accuracy)
[![paper trades](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcryptos.broker%2Fapi%2Fstrategies%2Flab-record&query=%24.paper_trades_total&label=paper%20trades%20published&color=a78bfa&style=flat-square)](https://cryptos.broker/api/strategies)
[![strategies listed](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fcryptos.broker%2Fapi%2Fstrategies%2Flab-record&query=%24.listed&label=strategies%20listed&color=ffa502&style=flat-square)](https://cryptos.broker/strategies)

*Those badges are fetched live from the public API every time this page loads. If one reads
`inaccessible`, the API is down and you are seeing that fact rather than a number we typed in
once and forgot.*

</div>

---

## Start here: the number most platforms hide

Every strategy CRYPTOS has ever published, forward-tracked on paper, winners and losers in
one table:

<!-- LIVE:record -->
| | |
|---|---|
| Strategies listed | **32** |
| Proven | **5** |
| **Retired / removed** | **35** |
| **Underperforming, still listed** | **12** |
| Forward paper trades recorded | **2,262** |
| Evaluated strategies that are net positive | **14 of 31** |
| **Average net result across all evaluated** | **-9.5%** |
<!-- /LIVE:record -->

That average is negative, it is at the top of this README, and it is
**[live at `/api/strategies/lab-record`](https://cryptos.broker/api/strategies/lab-record)** —
recomputed from the database on every request, so it cannot be quietly improved. The table
above is regenerated from that endpoint by a scheduled job, not typed by hand.

The retired experiments are published with their reasons. The largest, in full:

> **Top Picks — daily candidate generator.** Retired 2026-07-17. 122 resolved signals
> returned **+0.96R in total** — no edge — and **113 of the 122 were short during a rising
> market**. Shut off. The 29 picks still open at retirement were **voided rather than
> resolved**, so no outcome is invented from hindsight.

Anyone can show you winners. The reason to keep reading is that the losers are in the same
table, with the same denominator.

### The AI publishes its own report card too

<!-- LIVE:calibration -->
| Model confidence | 4-day directional hit rate | Sample |
|---|---|---|
| 0.0–0.2 | 47.5% | 1,697 |
| 0.2–0.4 | 49.2% | 3,389 |
| 0.4–0.6 | 50.7% | 7,661 |
| 0.6–0.8 | 52.9% | 21,202 |
| **0.8–1.0** | **54.1%** | 4,486 |

*38,435 scored forecasts over 180 days. Headline hit rate: 52.0%.*
<!-- /LIVE:calibration -->

The headline hit rate is barely better than a coin flip, and we publish that instead of
hiding it. **The bucket breakdown is the actual finding:** the hit rate climbs with the
model's own stated confidence. That is calibration evidence — it means the confidence score
carries real information, so you can act on the top bucket rather than the average. You could
not check that claim if only the headline were published, which is why the buckets are.

---

## Why this exists

Serious positioning data is priced for institutions and sold in pieces. Funding analytics is
one subscription. On-chain is another. A smart-money tracker is a third. A backtester is a
fourth. Each has its own login and its own bill, and none of them talk to each other — so you
end up as the integration layer, holding six tabs open and reconciling them by eye.

CRYPTOS is the argument that a single operator with direct exchange feeds and no incentive to
upsell can put the whole picture on one screen. **No inside connections, no institutional
minimum, no sales call.** Everything below is either free to anyone with a browser, or
included in one subscription.

---

## What's free (no account required)

Real data to anonymous callers. No sign-up, no key, no email. Every endpoint here was
verified to return `200` to a fresh anonymous request from the open internet.

<!-- LIVE:market -->
**308 live markets** · **$13.6B** open interest · **9,135** quality-scored traders tracked of 18,232
<!-- /LIVE:market -->

| What | Where |
|---|---|
| **Global market stats** — total OI, live market count, average funding, BTC dominance | [`/api/market/global`](https://cryptos.broker/api/market/global) |
| **Daily digest** — biggest movers, funding extremes, macro regime, next macro event | [`/api/market/today`](https://cryptos.broker/api/market/today) |
| **Market overview** — every live market with price, OI, funding | [`/api/market/overview`](https://cryptos.broker/api/market/overview) |
| **Funding extremes** — the most crowded longs and shorts | [`/api/market/funding/extremes`](https://cryptos.broker/api/market/funding/extremes) |
| **AI forecast accuracy** — hit rate by confidence bucket | [`/api/kronos/accuracy`](https://cryptos.broker/api/kronos/accuracy) |
| **Every strategy's full record** — IS/OOS metrics and live paper results, *including the underperformers* | [`/api/strategies`](https://cryptos.broker/api/strategies) |
| **The lab record** — the aggregate above | [`/api/strategies/lab-record`](https://cryptos.broker/api/strategies/lab-record) |
| **BTC cycle summary** — cycle quality score, zone, age | [`/api/cycle/btc/summary`](https://cryptos.broker/api/cycle/btc/summary) |
| **BTC on-chain** — live node data | [`/api/market/btc/onchain`](https://cryptos.broker/api/market/btc/onchain) |
| **BTC seasonality** — today's historical edge, with sample size | [`/api/market/btc/seasonality/today`](https://cryptos.broker/api/market/btc/seasonality/today) |
| **Macro regime** — the current growth/inflation quadrant | [`/api/market/macro`](https://cryptos.broker/api/market/macro) |
| **CRYPTOS Campus** — full trading curriculum, free, no account | [cryptos.broker/campus](https://cryptos.broker/campus) |
| **Methodology** — how every signal is built and validated | [cryptos.broker/methodology](https://cryptos.broker/methodology) |

Full reference with response shapes: **[`docs/api.md`](docs/api.md)**.
Python client: **[`client/`](client/)** — standard library only, nothing to install.

### The free tier is deliberately a real tier

Free is not a teaser that shows an empty chart and asks for a card. **The entire published
track record is free — including the parts that make CRYPTOS look bad** — because a record
you can only see after paying isn't a record, it's a brochure. The whole Campus curriculum is
free for the same reason.

What Pro buys is the **live signal**: not *what happened*, but *what is firing right now*.

---

## What Pro adds

A 7-day free trial, cancel anytime, nothing charged before the trial ends.
**[Current pricing →](https://cryptos.broker)**

| | |
|---|---|
| **Operator cockpit** | The EMA×Sigma Signal Board — every tracked asset ranked by proximity to firing, with entry, stop, target, R:R and real per-asset max leverage. It informs and recommends; **you make every call.** |
| **CRYPTOS AI** | A trading assistant wired to every live data point on the platform. |
| **Kronos AI predictions** | 1-day and 4-day forecasts across the tracked universe with confidence scores — and the [accuracy record](https://cryptos.broker/api/kronos/accuracy) is public, so you can price the confidence before you trust it. |
| **Full market depth** | Every live market with OI, funding, spread, supply/demand zones, relative strength vs BTC, project and community context. |
| **Active Alpha radar** | Funding extremes ranked by **z-score**, not raw rate — plus compression watch and a 15-minute execution-timing playbook by UTC hour. |
| **Smart Money Board** | Thousands of quality-scored traders, live positions and consensus positioning, refreshed every few minutes. |
| **Macro Regime dashboard** | A 5-layer synthesis into a TRADE / CAUTION / NO_TRADE permission gate. It vetoes exposure; it does not pick trades. |
| **Strategy backtester** | Visual builder, plain-English AI Assist, a 24-variation engine sweep, and walk-forward IS/OOS validation on held-out data. |
| **Slapper Library** | Certified strategies, re-validated on clean data, published only after review. |
| **Alerts** | Market conditions, strategy fires, AI-built custom logic — in-app, email, browser push, or Telegram. |
| **Events calendar** | FOMC, CPI, NFP, PCE and CME expiry, with quantified historical impact per event type across four time windows. |

Side-by-side breakdown: **[`docs/free-vs-pro.md`](docs/free-vs-pro.md)**.

---

## How it's built to not lie to you

Four rules the platform holds itself to. They are enforced in code, not promised in copy —
and this repository is held to them as well, which is why the numbers above are generated
rather than typed.

**1. Live-derived or absent.** Numbers are computed from the database at request time. When a
source fails, the page renders **without the number** rather than falling back to a stale
one. A gap is self-evidently a gap; a stale number is a lie with good posture.

**2. Zero assets is a failure to measure, never a measurement of zero.** If a pipeline breaks
and produces an empty result, the write is refused and the staleness alarm fires. Broken
systems are supposed to look broken.

**3. Published records include the failures, or they aren't records.** The underperforming
strategies stay listed with full metrics. Retired experiments keep their reasons attached.
Unresolved positions are **voided, never resolved from hindsight**, and reported separately
so the denominator can't be improved by dropping the unknowns.

**4. Descriptive surfaces never make calls.** The free daily digest reports what happened. It
does not rank setups or imply direction. Top Picks is what happened when a daily surface
started making calls it couldn't back — see the retirement notice above.

Written up in full at **[`docs/methodology.md`](docs/methodology.md)**.

---

## Quick start

```bash
git clone https://github.com/RWCS-LTD/cryptos-broker.git
cd cryptos-broker/client
python3 example.py          # no dependencies — standard library only
```

```python
from cryptos import CryptosClient

c = CryptosClient()

g = c.global_stats()
print(f"{g['assets_count']} live markets · ${g['total_oi']/1e9:.1f}B open interest")

for a in c.funding_extremes()["crowded_long"]:
    print(f"{a['asset']:<8} funding {a['funding']*100:+.4f}%  OI ${a['oi']/1e6:.1f}M")

acc = c.kronos_accuracy()["overall"]
print(f"AI forecast hit rate: {acc['hit_rate_4d']:.1%} over {acc['n_total']:,} predictions")
```

---

## Glossary

Plain-English definitions of the concepts this platform is built on — open interest, funding
rates and z-scores, order-block zones, walk-forward validation, macro regime, smart-money
positioning: **[`docs/glossary.md`](docs/glossary.md)**.

Starting from zero? The free [CRYPTOS Campus](https://cryptos.broker/campus) covers the same
ground properly, in order, with no account required.

---

## Links

| | |
|---|---|
| Platform | **[cryptos.broker](https://cryptos.broker)** |
| Track record | [cryptos.broker/strategies](https://cryptos.broker/strategies) |
| Methodology | [cryptos.broker/methodology](https://cryptos.broker/methodology) |
| Free curriculum | [cryptos.broker/campus](https://cryptos.broker/campus) |
| Contact | [cryptos.broker/contact](https://cryptos.broker/contact) |

---

## About this repository

The **public explainer and API client** for CRYPTOS. The platform itself — backend, frontend,
data pipeline and trading systems — is closed source and stays that way.

Nothing here requires credentials. Every documented endpoint already serves anonymous
requests from the open internet.

**On the numbers.** Every figure in this README is either *frozen history* (a closed record
that cannot change, such as a retired experiment's final tally) or *generated* from the live
API by [`scripts/refresh_live_numbers.py`](scripts/refresh_live_numbers.py), which runs daily
via GitHub Actions. There is deliberately no third category. If the API is unreachable the
job fails and writes nothing, rather than publishing zeros — see rule 2 above.

Client code is MIT licensed ([`LICENSE`](LICENSE)). Documentation and copy are CC BY 4.0
([`LICENSE-docs`](LICENSE-docs)).

*Live figures last refreshed: <!-- LIVE:stamp -->2026-08-23<!-- /LIVE:stamp --> (UTC).*

---

<div align="center">

**Not financial advice.** Rule-based systems validated on historical data. Past performance
does not guarantee future results. Every signal on this platform informs a decision — you
make the call.

</div>
