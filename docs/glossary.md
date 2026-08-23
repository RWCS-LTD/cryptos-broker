# Glossary

Plain-English definitions of the concepts CRYPTOS is built on. Written for
someone with no institutional background and no inside connections — which is
most people, and the whole reason the platform exists.

If you want this properly rather than as reference cards, the free
[CRYPTOS Campus](https://cryptos.broker/campus) covers the same ground in order,
with no account required.

**Contents:** [Perpetual futures](#perpetual-futures) ·
[Open interest](#open-interest-oi) · [Funding rate](#funding-rate) ·
[Funding z-score](#funding-z-score) · [Crowded positioning](#crowded-positioning) ·
[Liquidation](#liquidation) · [Mark price vs mid price](#mark-price-vs-mid-price) ·
[Order block](#order-block) · [Smart money](#smart-money) ·
[Macro regime](#macro-regime) · [Backtest](#backtest) ·
[In-sample vs out-of-sample](#in-sample-vs-out-of-sample-isoos) ·
[Walk-forward validation](#walk-forward-validation) ·
[Overfitting](#overfitting-curve-fitting) · [Profit factor](#profit-factor-pf) ·
[Recovery factor](#recovery-factor-rf) · [Max drawdown](#maximum-drawdown-dd) ·
[R multiple](#r-multiple) · [Paper trading](#paper-trading-forward-testing) ·
[Seasonality](#seasonality) · [HyperLiquid](#hyperliquid) · [HIP-3](#hip-3)

---

## Perpetual futures

A futures contract with **no expiry date**. You can hold it indefinitely.

Because it never settles, nothing naturally pulls its price toward the spot
price of the underlying asset — so exchanges add a mechanism that does: the
[funding rate](#funding-rate).

Perps are how most crypto leverage trading actually happens. When people say
"open interest" or "funding" in crypto, they are almost always talking about
perps.

## Open interest (OI)

**The total value of positions currently open** in a market — every contract
that has been opened and not yet closed.

Not volume. Volume counts trades over a period; open interest is a snapshot of
what is still on the table right now.

Why it matters:

- **Rising OI + rising price** — new money entering long. The move has fuel.
- **Rising OI + falling price** — new money entering short.
- **Falling OI + rising price** — shorts closing, not new buyers. A short
  squeeze, and it burns out when the shorts are done.
- **Falling OI + falling price** — longs capitulating.

Price alone cannot distinguish these four. That is the entire argument for
watching OI.

## Funding rate

The periodic payment between longs and shorts that keeps a perpetual's price
tethered to spot.

- **Positive funding** — longs pay shorts. The crowd is long, and it costs them
  to stay there.
- **Negative funding** — shorts pay longs. The crowd is short.

Two practical consequences:

**It is a cost.** A 0.05% daily funding rate on a $10,000 position is $5/day —
$150/month bleeding out of a position that hasn't moved. Know what a hold costs
before you enter it.

**It is a positioning gauge.** Sustained extreme funding means one side is
heavily crowded and paying for the privilege. That is where squeezes start.

Rates are returned as decimals: `0.0000408` means `+0.00408%`.

## Funding z-score

**How unusual today's funding rate is for that specific asset**, measured in
standard deviations from its own historical average.

This is the single most useful correction in the glossary. A raw funding rate is
close to meaningless in isolation:

| Asset | Funding now | Its normal range | Raw rate says | Z-score says |
|---|---|---|---|---|
| A | +0.03% | +0.02% to +0.06% | "high" | perfectly ordinary |
| B | +0.03% | −0.01% to +0.01% | "high" | **extreme** |

Same number, opposite meanings. Sorting a funding screener by raw rate gives you
a list of assets that always have high funding — which is not information.
Sorting by z-score gives you assets doing something *unusual for them*.

CRYPTOS Pro ranks funding extremes by z-score. The free endpoint returns raw
rates.

## Crowded positioning

When a large majority of open interest sits on one side of a market, evidenced
by sustained extreme [funding](#funding-rate).

Crowded positioning is not itself a signal to fade. Crowds are right during
trends, and "everyone is long" can stay true for months. What it does establish
is **fragility**: when a crowded market moves against the crowd, forced
[liquidations](#liquidation) add fuel in the same direction, so the move goes
further and faster than the news deserves.

## Liquidation

The forced closing of a leveraged position when its margin no longer covers its
losses. The exchange closes it at market, whatever the price.

Liquidations cluster at predictable price levels, and each one is a market order
in the direction that is already hurting. This is the mechanism that turns an
ordinary move in a [crowded](#crowded-positioning) market into a cascade.

## Mark price vs mid price

**Mid price** — the midpoint between the best bid and best ask. What the market
is quoting.

**Mark price** — the exchange's own reference price, usually smoothed and
anchored to a broader index. Liquidations are calculated against the mark, not
the mid, specifically so a thin orderbook can't be pushed a few percent to
trigger a cascade.

If you are calculating where a position gets liquidated, use the mark.

## Order block

A price zone where a large amount of activity previously occurred and price
reacted sharply away from it — the footprint of size entering the market.

The reasoning: an institution that filled a large position in a zone has an
interest in defending it, and unfilled orders may remain there. When price
returns, the zone often acts as support or resistance.

**Demand zone** — below price, where buying previously appeared.
**Supply zone** — above price, where selling previously appeared.

Order blocks are a *structural* input, not a signal on their own. In CRYPTOS
they combine with momentum and regime, because a zone that lines up with a
trend is a very different proposition from one that fights it.

## Smart money

Wallets with a demonstrated record of profitable positioning, identified
on-chain and tracked continuously.

The concept is frequently abused. Two things make it meaningful rather than
decorative:

1. **Quality scoring** — a wallet must clear a performance bar before it counts,
   otherwise you are tracking noise with an impressive name. CRYPTOS tracks tens
   of thousands of wallets and qualifies only a fraction of them.
2. **Consensus, not individuals** — one whale is an anecdote. Agreement *across*
   scored wallets is the actual signal.

You still cannot see intent. A large short may be a directional bet or a hedge
against spot held elsewhere. Positioning data narrows the possibilities; it
does not read minds.

## Macro regime

A classification of the broad economic environment — typically along growth and
inflation axes — that sets which trades are worth taking at all.

The point of a regime layer is **permission, not selection**. It answers "should
I have exposure right now?" and never "which asset should I buy?". A signal that
looks excellent in isolation may be one you should skip because the environment
is hostile to the whole class of trade.

CRYPTOS synthesises five layers into a `TRADE` / `CAUTION` / `NO_TRADE` gate.
The gate can veto exposure; it does not pick trades.

## Backtest

Running a set of trading rules over historical data to see what it would have
returned.

Necessary, and treacherous. A backtest is a **lower bound on your creativity,
not an upper bound on your returns**: it is trivial to produce a beautiful
equity curve by trying variations until one fits the past. Everything below
exists to separate a real edge from that.

## In-sample vs out-of-sample (IS/OOS)

**In-sample** — the data you used while building and tuning the strategy.
**Out-of-sample** — data the strategy never saw during development.

In-sample results are close to worthless on their own. You chose the rules
*because* they worked on that data; of course they worked on that data.

Out-of-sample results are the first honest evidence. CRYPTOS publishes both for
every strategy, so you can see the gap.

## Walk-forward validation

Splitting history into consecutive segments, training on one and testing on the
next, repeatedly — rather than testing once on a single held-out block.

CRYPTOS uses a **60% train / 20% validation / 20% held-out test** split. The
best variant found in training is then tested **blind** on the held-out portion.

The number to look for is **decay**: how much performance drops from in-sample
to out-of-sample. Large decay means the strategy learned the past rather than
the market. A rule that survives walk-forward has at least demonstrated it works
on data it was not shaped by.

## Overfitting (curve fitting)

Tuning a strategy until it fits historical noise instead of a real pattern.

The tell is fragility: an overfit strategy's results collapse when you change a
parameter slightly, shift the date range, or run it on a different asset. A real
edge degrades gracefully. An overfit one falls off a cliff.

This is why CRYPTOS sweeps every strategy across 24 variations of direction, DCA
mode, exit logic and stop/target — a rule that only works at exactly one
parameter setting has told you what it is.

## Profit factor (PF)

**Gross profit ÷ gross loss.**

- `PF = 1.0` — breakeven before costs.
- `PF = 1.2` — a common minimum bar.
- `PF > 2.0` — strong, and worth double-checking for [overfitting](#overfitting-curve-fitting).
- `PF = ∞` — no losing trades, which almost always means the sample is too small
  to mean anything.

Always read PF next to the trade count. A profit factor over 8 trades is noise.

## Recovery factor (RF)

**Net profit ÷ maximum drawdown.**

It answers the question return alone can't: *what did you go through to get it?*
A strategy returning 40% with a 10% drawdown (RF 4.0) and one returning 40% with
a 35% drawdown (RF 1.14) have identical returns and are not remotely the same
product. The second one is far harder to actually hold.

## Maximum drawdown (DD)

**The largest peak-to-trough decline** in an equity curve, as a percentage.

The most under-weighted number in trading. It is the number that determines
whether you can actually run a strategy, because it describes the worst stretch
you must sit through without abandoning it.

## R multiple

**Profit or loss expressed in units of the risk taken on that trade.**

If you risk $100 and make $250, that is +2.5R. Risk $100 and get stopped out,
that is −1R.

R normalises across position sizes, so a record in R is comparable across trades
in a way a record in dollars is not. "+0.96R over 122 signals" — the retired
Top Picks record in this repository's README — means 122 signals collectively
returned less than a single winning trade's typical result. That is how you say
"no edge" precisely.

## Paper trading (forward testing)

Recording what a strategy *would* have done, live, going forward — after
development is frozen.

This is the strongest evidence short of real money, because the strategy cannot
have been tuned to data that did not exist yet. It is also the slowest, which is
why it is rare to see published.

CRYPTOS forward-tracks every listed strategy and publishes the running record —
thousands of paper trades, winners and losers, at
[`/api/strategies`](https://cryptos.broker/api/strategies).

## Seasonality

Recurring calendar patterns in returns — specific days, months, or points in a
cycle that historically behaved differently from average.

Handle with care. With enough calendar slices you *will* find patterns in noise,
and Bitcoin has only about sixteen years of history — which means any given
calendar day has roughly sixteen samples. That is why the CRYPTOS seasonality
endpoint returns the sample count `n` alongside every average: so you can see
how thin the evidence is rather than having it hidden behind a single number.

## HyperLiquid

A decentralised perpetual futures exchange running on its own high-performance
L1 blockchain.

What makes it unusually good for analysis: **the orderbook and every position
are on-chain**. On a centralised exchange, positioning data is either sold to
you or not available at all. On HyperLiquid it is public infrastructure — which
is what makes wallet-level [smart money](#smart-money) tracking possible without
inside connections or an institutional data contract.

## HIP-3

The HyperLiquid standard that allows permissionless deployment of new perpetual
markets, including markets on **non-crypto** underlyings.

In practice this means tokenised equities, indices, metals, energy and FX trade
on the same venue, with the same [open interest](#open-interest-oi) and
[funding](#funding-rate) data as the crypto perps. You can look at gold, the
S&P, and Bitcoin positioning through one lens, on one screen, from one API.

---

*Concepts you'd like added? [Get in touch](https://cryptos.broker/contact).*
