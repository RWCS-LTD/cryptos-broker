# CRYPTOS public API

Base URL: `https://cryptos.broker/api`

No API key. No account. No registration. Every endpoint below serves anonymous
requests over the open internet.

A Python client covering all of these lives in [`../client/`](../client/) —
standard library only, nothing to install.

---

## Conventions

**Response envelope.** Some endpoints wrap their payload, others return it
directly:

```jsonc
// wrapped — most /market/* endpoints
{ "data": { ... }, "meta": { "last_updated": "...", "age_seconds": 119, "is_stale": false } }

// direct — /market/today, /strategies, /cycle/*
{ "as_of": "...", "movers_up": [ ... ] }
```

The client's methods normalise this for you.

**`meta.is_stale`.** Where present, this is the API telling you the underlying
data is older than that endpoint's freshness threshold. **Check it.** A stale
funding rate is worse than no funding rate, because it looks current.

**Degraded responses, not 500s.** If an upstream source fails, endpoints return
a degraded response — typically `data: null` — rather than an error. Handle
`null` as a real possibility on every field.

**`limited: true`.** Some endpoints truncate for anonymous callers and say so
explicitly in the response body. It is a documented boundary, not a silent one.

**Rate limiting.** Applied per IP. Be reasonable: cache locally, don't poll in a
tight loop. The data behind most of these refreshes on the order of minutes, so
polling faster than that gets you the same bytes back.

**Compression.** Responses over 1KB are gzipped. Send
`Accept-Encoding: gzip` — several of these payloads are large.

---

## Market

### `GET /market/global`

Exchange-wide totals.

```bash
curl -s https://cryptos.broker/api/market/global
```

| Field | Meaning |
|---|---|
| `assets_count` | Live markets. Delisted markets (zero price *and* zero OI) are filtered out. |
| `total_oi` | Total open interest across the exchange, USD. |
| `avg_funding` | Average funding rate as a decimal — `0.0000408` is `+0.00408%`. |
| `btc_dominance` | BTC share of estimated global market cap, percent. |
| `tracked_traders` / `qualified_traders` | Wallets tracked, and the subset that clear the quality score. |
| `btc_mcap_sparkline` | Recent BTC market-cap series for charting. |

### `GET /market/today`

The free daily digest — biggest movers, funding extremes, macro regime, next
macro event.

**Descriptive only.** It reports what happened. It does not rank setups or imply
direction, by design — see [methodology](methodology.md#4-descriptive-surfaces-never-make-calls).

| Field | Meaning |
|---|---|
| `crypto_perps_scanned` | Markets included in this digest. |
| `movers_up` / `movers_down` | Largest 24h moves, each with `change_24h`, `funding`, `oi_usd`. |
| `funding_paying_longs` / `funding_paying_shorts` | Where positioning is most expensive to hold. |
| `macro_regime` | Current regime label, or `null`. |
| `next_event` | Next scheduled macro event with `title` and `days_away`. |

### `GET /market/overview`

Every live market with price, open interest and funding. The bulk endpoint —
expect a large gzipped payload.

### `GET /market/funding/extremes`

The most crowded longs and shorts.

```jsonc
{
  "data": {
    "crowded_long":  [ { "asset": "APEX", "funding": 0.000335, "oi": 6530802.0, "mid": 0.2718 } ],
    "crowded_short": [ { "asset": "ACE",  "funding": -0.000733, "oi": 8782068.3, "mid": 0.2312 } ]
  },
  "limited": true
}
```

Positive funding means longs pay shorts — the crowd is long and it costs them to
stay there. Anonymous callers get a truncated list (`limited: true`).

**Pro ranks the full set by z-score rather than raw rate.** That difference
matters more than it sounds: a `+0.03%` rate is unremarkable on an asset that
normally runs `+0.05%`, and extreme on one that normally sits at zero. The raw
rate cannot tell you which you're looking at. See
[glossary → funding z-score](glossary.md#funding-z-score).

### `GET /market/macro`

Current macro regime — the growth/inflation quadrant classification, with a
headline string and display colour.

---

## Bitcoin

### `GET /cycle/btc/summary`

| Field | Meaning |
|---|---|
| `cqm_score` | Cycle quality score, 0–100. |
| `cycle_zone` | Zone label — e.g. `buy`, `neutral`, `sell`. |
| `cycle_age_days` | Days since the last halving. |
| `halving_number` | Which halving epoch. |
| `current_price` | BTC price at last computation. |

### `GET /market/btc/onchain`

Live on-chain data from a Bitcoin node.

### `GET /market/btc/seasonality/today`

Historical average return for today's calendar date and the days that follow.

```jsonc
{ "data": [ { "date": "Aug 23", "label": "Today", "avg_pct": 0.53, "n": 16 } ] }
```

**Read `n` before `avg_pct`.** Sixteen samples of one calendar day is a
curiosity, not an edge. The field is returned precisely so the sample size
cannot be hidden behind the average.

The full 12×31 heatmap is Pro.

---

## Track record

These are the endpoints that make the platform auditable. They are public on
purpose — see [methodology](methodology.md).

### `GET /kronos/accuracy`

Published accuracy of the Kronos AI forecasts.

```jsonc
{
  "data": {
    "overall": { "n_total": 38435, "hit_rate_4d": 0.52, "lookback_days": 180 },
    "buckets": [ { "bucket": "0.8–1.0", "hit_rate_4d": 0.541, "n_total": 4486 } ],
    "per_asset": [ ... ]
  }
}
```

**The buckets are the point, not the overall number.** A 52% overall hit rate is
barely a coin flip. What makes the forecast usable is that the hit rate climbs
monotonically with the model's own stated confidence — so the confidence score
carries real information, and you can act on the top bucket rather than the
average.

Kronos is a third-party open-source model. **The proprietary asset is the
measurement, not the model** — which is why the measurement is public.

Per-asset predictions and per-symbol accuracy are Pro.

### `GET /strategies`

Every listed strategy with full metrics.

| Field group | Fields |
|---|---|
| Identity | `id`, `strategy_name`, `assets`, `timeframe`, `description` |
| In-sample | `is_rf`, `is_pf`, `is_ret`, `is_dd`, `is_wr` |
| Out-of-sample | `oos_rf`, `oos_pf`, `oos_dd` |
| Live paper record | `paper_started_at`, `paper_trades`, `paper_net_pct`, `paper_win_rate`, `paper_pf`, `paper_max_dd` |
| State | `status`, `updated_at` |

**Includes the underperformers.** Twelve of the currently listed strategies are
classified `underperforming` and keep their full metrics on display.

Pro adds `params` (the actual rule set), `last_signal`, `last_signal_at`,
`live_status`, the signal feed and open positions. The public field set is an
allowlist, so a new database column cannot leak into this response by default.

### `GET /strategies/lab-record`

The aggregate across every strategy ever published.

| Field | Meaning |
|---|---|
| `listed` | Currently listed. |
| `by_state` | Counts per lifecycle state — `certified`, `monitoring`, `proven`, `underperforming`, `retired`, `removed`. |
| `paper_trades_total` | Forward paper trades recorded. |
| `evaluated` / `evaluated_positive` | How many have enough data to judge, and how many are net positive. |
| `net_pct_avg`, `net_pct_best`, `net_pct_worst` | Net result across evaluated strategies. |
| `retired_experiments` | Each retired experiment with `n_resolved`, `total_r`, `voided_unresolved`, and `why`. |

`voided_unresolved` exists so the denominator cannot be quietly improved by
dropping positions that were still open when an experiment was shut off.

---

## Health

### `GET /health`

Liveness check.

---

## Not documented here

Pro endpoints — the operator cockpit, live signals, Kronos predictions, the
smart-money board, the trader leaderboard, alerts, the backtester — require an
authenticated Pro session. They are out of scope for this client by design.

See [free vs Pro](free-vs-pro.md).
