#!/usr/bin/env python3
"""
CRYPTOS public API — worked example.

Run it:  python3 example.py

No dependencies, no API key, no account. Everything printed here comes from
endpoints that serve anonymous requests.
"""

from cryptos import CryptosClient, CryptosError


def rule(title: str) -> None:
    print(f"\n\033[1m{title}\033[0m\n" + "─" * 64)


def main() -> int:
    c = CryptosClient()

    # ── the market right now ───────────────────────────────────────────────
    rule("MARKET")
    g = c.global_stats()
    print(f"  Live markets      {g['assets_count']}")
    print(f"  Open interest     ${g['total_oi'] / 1e9:,.2f}B")
    print(f"  Average funding   {g['avg_funding'] * 100:+.4f}%")
    print(f"  BTC dominance     {g['btc_dominance']:.1f}%")
    print(f"  Traders scored    {g['qualified_traders']:,} of {g['tracked_traders']:,} tracked")

    # ── who is paying whom ─────────────────────────────────────────────────
    # Positive funding = longs pay shorts, i.e. the crowd is long and it costs
    # them to stay there. Persistent extremes are where squeezes start.
    rule("MOST CROWDED POSITIONING")
    fx = c.funding_extremes()
    for side, label in (("crowded_long", "Longs paying"), ("crowded_short", "Shorts paying")):
        print(f"  {label}:")
        for a in fx.get(side, []):
            print(
                f"    {a['asset']:<8} {a['funding'] * 100:+8.4f}%   "
                f"OI ${a['oi'] / 1e6:,.1f}M   ${a['mid']:,.4f}"
            )

    # ── today's movers ─────────────────────────────────────────────────────
    rule("TODAY")
    t = c.today()
    print(f"  Scanned {t['crypto_perps_scanned']} perps · macro regime: {t.get('macro_regime') or 'n/a'}")
    ups = ", ".join(f"{m['asset']} {m['change_24h']:+.1f}%" for m in t["movers_up"][:3])
    downs = ", ".join(f"{m['asset']} {m['change_24h']:+.1f}%" for m in t["movers_down"][:3])
    print(f"  Up      {ups}")
    print(f"  Down    {downs}")
    if t.get("next_event"):
        e = t["next_event"]
        print(f"  Next    {e['title']} in {e['days_away']}d")

    # ── bitcoin cycle ──────────────────────────────────────────────────────
    rule("BITCOIN CYCLE")
    cy = c.btc_cycle()
    print(f"  Price             ${cy['current_price']:,.0f}")
    print(f"  Cycle zone        {cy['cycle_zone'].upper()}  (quality score {cy['cqm_score']})")
    print(f"  Cycle age         {cy['cycle_age_days']} days since halving #{cy['halving_number']}")

    # ── the AI's own report card ───────────────────────────────────────────
    # Published so you can price the confidence before trusting it. Compare
    # `hit_rate_4d` across buckets: if the model's confidence is meaningful,
    # the high-confidence bucket beats the low one.
    rule("AI FORECAST ACCURACY (published)")
    acc = c.kronos_accuracy()
    o = acc["overall"]
    print(f"  {o['n_total']:,} scored predictions over {o['lookback_days']} days")
    print(f"  4-day directional hit rate   {o['hit_rate_4d']:.1%}")
    print(f"  ...at the confidence threshold {o['hit_rate_4d_thresholded']:.1%}")
    print("  By confidence bucket:")
    for b in acc["buckets"]:
        print(f"    {b['bucket']:<12} {b['hit_rate_4d']:.1%}   n={b['n_total']:,}")

    # ── the full record, losers included ───────────────────────────────────
    rule("STRATEGY TRACK RECORD (losers included)")
    lab = c.lab_record()
    print(f"  Listed            {lab['listed']}")
    print(f"  Proven            {lab['proven']}")
    print(f"  Retired           {lab['retired']}")
    print(f"  Paper trades      {lab['paper_trades_total']:,}")
    print(f"  Net positive      {lab['evaluated_positive']} of {lab['evaluated']} evaluated")
    if lab.get("net_pct_avg") is not None:
        print(f"  Average net       {lab['net_pct_avg']:+.1f}%")
        print(f"  Best / worst      {lab['net_pct_best']:+.1f}% / {lab['net_pct_worst']:+.1f}%")

    for exp in lab.get("retired_experiments", []):
        print(f"\n  \033[2mRetired — {exp['name']} ({exp['retired_at']})\033[0m")
        print(f"  \033[2m{exp['why']}\033[0m")

    print("\n" + "─" * 64)
    print("  Full platform: https://cryptos.broker")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CryptosError as exc:
        print(f"\nAPI error: {exc}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        raise SystemExit(130)
