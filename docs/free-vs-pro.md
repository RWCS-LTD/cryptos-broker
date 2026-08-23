# Free vs Pro

**Free** — no account, no card, no email. Open a browser or call the API.
**Pro** — $29.99/month or $299/year (save 17%). 7-day free trial, cancel
anytime, nothing charged before the trial ends.

---

## The line, in one sentence

> **Free gives you the record. Pro gives you the live signal.**

Everything CRYPTOS has already done — every strategy's full result, the AI's
measured accuracy, the experiments that failed and why — is free to read without
an account. What you pay for is what is firing *right now*, and the tooling to
act on it.

That split is deliberate. A track record you can only see after paying is not a
record, it's a brochure.

---

## Side by side

| | Free | Pro |
|---|---|---|
| **Market data** | | |
| Global stats — OI, funding, market count, dominance | ✅ | ✅ |
| Daily digest — movers, funding extremes, regime, next event | ✅ | ✅ |
| Market overview — every live market | ✅ | ✅ |
| Full per-asset depth — spread, supply/demand zones, relative strength vs BTC, project context | — | ✅ |
| Funding extremes | Truncated list, raw rate | Full set ranked by **z-score**, plus compression watch |
| 15-minute execution-timing playbook by UTC hour | — | ✅ |
| **Track record** | | |
| Every strategy's IS/OOS metrics + live paper record | ✅ | ✅ |
| The underperforming strategies | ✅ | ✅ |
| Retired experiments with reasons | ✅ | ✅ |
| AI forecast accuracy by confidence bucket | ✅ | ✅ |
| Strategy rule sets (`params`) | — | ✅ |
| Last signal, live status, open positions | — | ✅ |
| **Signals & tooling** | | |
| Operator cockpit — EMA×Sigma Signal Board with entry/stop/target/RR | — | ✅ |
| Kronos AI predictions — 1D/4D across 250+ assets | Accuracy only | Predictions + per-asset accuracy |
| Smart Money Board — 9,000+ scored traders, live positions, consensus | — | ✅ |
| Top Traders leaderboard with equity curves | — | ✅ |
| Macro Regime dashboard — 5-layer TRADE / CAUTION / NO_TRADE gate | Regime label only | Full 5-layer synthesis |
| CRYPTOS AI assistant | — | ✅ |
| Strategy backtester — visual builder, AI Assist, walk-forward OOS | — | ✅ |
| Slapper Library — certified strategies, Clap/Fork/Follow | — | ✅ |
| Alerts — market, strategy, AI-built; in-app/email/push/Telegram | — | ✅ |
| Events calendar + quantified historical impact | Next event only | 60-day calendar, AI briefings, pre-event alerts, 6-asset impact heatmap |
| BTC seasonality | Today + following days | Full 12×31 heatmap |
| **Learning** | | |
| CRYPTOS Campus — 102-lesson curriculum | ✅ | ✅ |
| Campus AI tutor | ✅ | ✅ |
| Graduation certificate | ✅ | ✅ |
| Methodology documentation | ✅ | ✅ |

---

## What Pro actually costs you elsewhere

The components of this exist as separate products. Assembled, they run
**$39–129/month each**:

| You'd otherwise buy | For |
|---|---|
| A funding & OI analytics subscription | Positioning data |
| An on-chain data subscription | Cycle and network signals |
| A smart-money / whale tracker | Wallet positioning |
| A backtesting platform | Strategy validation |
| A macro calendar with impact data | Event risk |

Five logins, five bills, and you are the integration layer holding six tabs open
and reconciling them by eye. CRYPTOS is one subscription at **$29.99/month**
with the pieces already wired together.

---

## What Pro is not

**It is not a signal service that trades for you.** The Operator cockpit ranks
assets by proximity to firing and shows entry, stop, target and R:R. It informs
and it recommends. **You make every call.**

**It is not a guarantee.** Read the [lab record](https://cryptos.broker/api/strategies/lab-record)
before you pay — it is public, it includes the failures, and the average across
all evaluated strategies is currently negative. That number is on the front page
of this repository for the same reason it is in the API: you should price the
product with it in hand.

**It is not a lock-in.** 7-day trial, cancel from the account page, no call.

---

## Getting started free

1. Call the API — [`../client/`](../client/), no key, no account:
   ```bash
   cd client && python3 example.py
   ```
2. Read the record — [cryptos.broker/strategies](https://cryptos.broker/strategies)
3. Learn the concepts — [cryptos.broker/campus](https://cryptos.broker/campus), 102 free lessons
4. Understand the method — [cryptos.broker/methodology](https://cryptos.broker/methodology)

If the free surface is useful and you want the live signal,
[start the trial](https://cryptos.broker).
