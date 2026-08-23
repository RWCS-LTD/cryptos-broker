# Methodology

How CRYPTOS decides what to publish, and the rules it holds itself to.

The full technical write-up lives at
[cryptos.broker/methodology](https://cryptos.broker/methodology). This page
covers the principles — the ones that constrain what the platform is allowed to
show you.

---

## The problem this is a response to

Trading platforms have a structural incentive to look good. Nobody subscribes to
a dashboard that admits its signals didn't work. So the industry converged on a
set of habits that are technically honest and practically misleading:

- Publish the winners, quietly delist the losers.
- Show backtests, not forward results.
- Resolve open positions after the fact, once you know how they turned out.
- When a data feed breaks, show the last good number rather than a gap.
- Report a metric without the sample size behind it.

None of these is a lie. All of them produce a picture that is wrong. The four
rules below exist to make each one impossible rather than merely discouraged.

---

## 1. Live-derived or absent

**Every number is computed from the database at request time. When a source
fails, the number is omitted — never replaced with a stale fallback.**

A hardcoded number that was true when it was typed will keep rendering long
after it stops being true, and nothing will alert anyone, because a plausible
number looks exactly like a correct one. Prose is where this hides best: a
"330+ markets" claim typed into a landing page drifts silently for months.

So the landing page derives its market count from the live API, and when that
call fails it renders the sentence **without a number** rather than with an old
one. A gap is self-evidently a gap. A stale number is a lie with good posture.

The same rule governs pricing: the displayed price and the annual saving are
computed from a single source and cross-checked against the live payment
processor, because advertising less than you charge is a consumer-law problem
rather than a typo.

## 2. Zero is a failure to measure, never a measurement of zero

**When a pipeline produces an empty result, the write is refused and the
staleness alarm fires.**

This one came from a real failure. A scoring pipeline lost a dependency and
began publishing an *empty but freshly-timestamped* result. Every staleness
check keyed on the timestamp, so everything passed — while the actual content
was nothing at all. A broken system produced a clean bill of health.

The fix generalises: a fallback must not be indistinguishable from a
measurement. If the system cannot measure something, it must say so and let the
alarm fire, not publish an empty answer that satisfies its own monitoring.

## 3. Published records include the failures, or they aren't records

**Showing only the winners is the violation.**

Concretely, this means:

- The **underperforming strategies stay listed**, with full metrics, in the same
  table and the same denominator as the winners.
- **Retired experiments keep their reasons attached.** The largest is published
  in full: a daily candidate generator that produced 122 resolved signals for
  **+0.96R total** — no edge — with **113 of the 122 short during a rising
  market**. It was shut off, and the notice explaining why is public.
- **Unresolved positions are voided, never resolved from hindsight.** When that
  experiment was retired, 29 picks were still open. Resolving them using five
  weeks of hindsight would have fabricated outcomes into a published record. They
  are reported as `voided_unresolved`, in a separate field, so the denominator
  cannot be improved by dropping the unknowns.
- **The aggregate is public even though it's negative.** The average net result
  across all evaluated strategies is negative, it is on the front page of this
  repository, and it is live at
  [`/api/strategies/lab-record`](https://cryptos.broker/api/strategies/lab-record)
  — regenerated from the API rather than typed, so it cannot drift into flattery.

Publishing an unflattering number is not modesty. It is the only thing that
makes the flattering numbers worth reading, because it demonstrates that the
flattering ones weren't selected.

## 4. Descriptive surfaces never make calls

**A surface that reports conditions must not imply direction.**

The free daily digest lists movers, funding extremes, the current regime and the
next event. It does not rank setups and does not suggest what to do, because it
does not have the analysis behind it to justify a call.

This is the direct lesson of the retired experiment above. A daily surface that
started ranking candidates ended up **short 113 times out of 122 during a rally**
— it was not a market view that went wrong, it was a surface making calls it
could not back, published on a daily cadence because the cadence existed.

The signals that *do* make calls live behind Pro, carry entry, stop, target and
R:R, and are forward-tracked with their results published either way.

---

## How a strategy gets published

1. **Rule definition.** A hypothesis expressed as mechanical entry, exit and
   direction logic. No discretion.
2. **Variation sweep.** 24 combinations of direction, DCA mode, exit logic and
   stop/target. A rule that works at exactly one parameter setting has told you
   it is [overfit](glossary.md#overfitting-curve-fitting).
3. **Walk-forward validation.** 60% train / 20% validation / 20% held-out test.
   The best variant is tested **blind** on data it never saw.
4. **Gates.** Out-of-sample [recovery factor](glossary.md#recovery-factor-rf),
   [profit factor](glossary.md#profit-factor-pf), trade count and decay must all
   clear fixed thresholds. **The thresholds are frozen and are not lowered to
   let a candidate through.** An empty queue is the correct outcome when nothing
   qualifies.
5. **Adversarial review.** A candidate is argued against before it is banked.
   Most are correctly rejected here.
6. **Forward paper tracking.** Published, tracked live, results recorded whether
   they are good or bad.
7. **Lifecycle.** `certified` → `monitoring` → `proven`, or →
   `underperforming` → `retired`. Every state is visible in
   [`/api/strategies`](https://cryptos.broker/api/strategies).

Most candidates die at step 4 or 5. That is the process working.

---

## What this does not claim

**Not a guarantee.** Rule-based systems validated on historical data. Past
performance does not guarantee future results.

**Not automation.** Every signal informs a decision. You make the call.

**Not omniscience.** Positioning data narrows possibilities; it does not reveal
intent. A large short may be directional or a hedge against spot held elsewhere,
and no dataset here can tell you which.

**Not a claim of edge in the aggregate.** The published average across evaluated
strategies is negative. The argument is not "every strategy here makes money" —
it is "you can see exactly which ones did, on the same page, with the same
denominator, before you pay."

---

*Full technical documentation: [cryptos.broker/methodology](https://cryptos.broker/methodology)*
