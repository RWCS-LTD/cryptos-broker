# CRYPTOS Python client

A dependency-free client for the free [CRYPTOS](https://cryptos.broker) API.

**No API key. No account. No `pip install`.** Standard library only, Python 3.9+.

```bash
python3 example.py
```

---

## Use it

Copy `cryptos.py` next to your code, or add this directory to your path.

```python
from cryptos import CryptosClient

c = CryptosClient()
```

### Market

```python
g = c.global_stats()
print(f"{g['assets_count']} live markets · ${g['total_oi']/1e9:.1f}B OI")

# Who is paying whom. Positive funding = longs pay shorts.
for a in c.funding_extremes()["crowded_long"]:
    print(f"{a['asset']:<8} {a['funding']*100:+.4f}%  OI ${a['oi']/1e6:.1f}M")

today = c.today()          # movers, funding extremes, regime, next event
markets = c.overview()     # every live market
regime = c.macro()         # growth/inflation quadrant
```

### Bitcoin

```python
cy = c.btc_cycle()
print(f"${cy['current_price']:,.0f} — {cy['cycle_zone']} zone, day {cy['cycle_age_days']}")

c.btc_onchain()
c.btc_seasonality()        # read `n` before trusting `avg_pct`
```

### Track record

```python
# The AI's own report card. The buckets matter more than the overall number:
# hit rate should climb with the model's stated confidence, or the confidence
# score isn't carrying information.
acc = c.kronos_accuracy()
for b in acc["buckets"]:
    print(f"{b['bucket']:<12} {b['hit_rate_4d']:.1%}  n={b['n_total']:,}")

# Every strategy, including the underperformers.
for s in c.strategies()["strategies"]:
    print(f"{s['strategy_name']:<40} OOS PF {s['oos_pf']}  paper {s['paper_net_pct']}%")

lab = c.lab_record()
print(f"{lab['evaluated_positive']}/{lab['evaluated']} net positive, avg {lab['net_pct_avg']:+.1f}%")
```

---

## Notes

**Errors.** Everything raises `CryptosError` on failure. Transport errors and
5xx responses are retried with linear backoff; 4xx responses are not, because a
403 will not become a 200 on the second attempt.

```python
from cryptos import CryptosClient, CryptosError

try:
    data = c.global_stats()
except CryptosError as exc:
    print(f"unavailable: {exc}")
```

**Nulls are real.** When an upstream source fails, endpoints return a degraded
response rather than a 500 — usually `data: null`, sometimes a null field.
Handle it.

**Staleness.** Several endpoints carry a `meta.is_stale` flag. The client
returns the unwrapped `data` from those, so if staleness matters to you, call
`client._get(path)` directly and read `meta` yourself. A stale funding rate is
worse than no funding rate, because it looks current.

**Rate limits.** Per IP. Cache locally and don't poll in a tight loop — most of
this data refreshes on the order of minutes, so a faster loop returns the same
bytes and nothing else.

**Truncation.** `funding_extremes()` returns a shortened list to anonymous
callers, flagged as `limited: true` in the raw response. Pro ranks the full set
by [z-score](../docs/glossary.md#funding-z-score) rather than raw rate.

---

Full endpoint reference: [`../docs/api.md`](../docs/api.md)
Licensed MIT. Not affiliated with HyperLiquid.
