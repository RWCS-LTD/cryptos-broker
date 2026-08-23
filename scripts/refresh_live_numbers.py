#!/usr/bin/env python3
"""
Regenerate the live-data blocks in README.md from the public CRYPTOS API.

Run by .github/workflows/refresh-live-numbers.yml on a daily schedule, and
runnable by hand:

    python3 scripts/refresh_live_numbers.py            # rewrite README.md
    python3 scripts/refresh_live_numbers.py --check    # exit 1 if stale, write nothing

Only content between paired markers is touched:

    <!-- LIVE:name --> ... <!-- /LIVE:name -->

Everything outside the markers is hand-written prose and is never modified.

────────────────────────────────────────────────────────────────────────────
THE RULE THIS SCRIPT EXISTS TO ENFORCE

A number typed into a README is true on the day it is typed and slowly becomes
a lie, with nothing to announce the transition. A plausible stale number is
worse than no number, because it looks exactly like a correct one.

So: numbers in this repository are either FROZEN HISTORY (a closed record that
cannot change — a retired experiment's final tally) or they are GENERATED HERE.
There is no third category, and in particular there is no "I'll remember to
update it" category.

Corollary, and the reason this script never writes a fallback: if the API is
unreachable or a field is missing, this script FAILS and writes nothing,
leaving the previous block in place for a human to notice. Publishing zeros
because the fetch failed would be a fabricated measurement — the precise
failure mode described in ../docs/methodology.md §2.
────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API = "https://cryptos.broker/api"
README = Path(__file__).resolve().parent.parent / "README.md"
TIMEOUT = 20.0


class RefreshError(RuntimeError):
    """Fetch failed or the payload was not shaped as expected."""


def fetch(path: str) -> Any:
    url = f"{API}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "cryptos-readme-refresh/1.0 (+https://github.com/RWCS-LTD/cryptos-broker)",
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return json.loads(raw.decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, OSError) as exc:
        raise RefreshError(f"GET {url} failed: {exc}") from exc


def need(obj: Any, *keys: str) -> Any:
    """Walk a nested payload, raising rather than defaulting on a missing key.

    `dict.get(k, 0)` is how a broken feed becomes a published zero. This is the
    opposite of that on purpose.
    """
    cur = obj
    for k in keys:
        if not isinstance(cur, dict) or k not in cur or cur[k] is None:
            raise RefreshError(f"missing field: {'.'.join(keys)}")
        cur = cur[k]
    return cur


# ── block builders ─────────────────────────────────────────────────────────

def build_record() -> str:
    lab = fetch("/strategies/lab-record")

    listed = need(lab, "listed")
    proven = need(lab, "proven")
    by_state = need(lab, "by_state")
    trades = need(lab, "paper_trades_total")
    evaluated = need(lab, "evaluated")
    positive = need(lab, "evaluated_positive")
    avg = need(lab, "net_pct_avg")

    retired = by_state.get("retired", 0) + by_state.get("removed", 0)
    under = by_state.get("underperforming", 0)

    return "\n".join([
        "| | |",
        "|---|---|",
        f"| Strategies listed | **{listed}** |",
        f"| Proven | **{proven}** |",
        f"| **Retired / removed** | **{retired}** |",
        f"| **Underperforming, still listed** | **{under}** |",
        f"| Forward paper trades recorded | **{trades:,}** |",
        f"| Evaluated strategies that are net positive | **{positive} of {evaluated}** |",
        f"| **Average net result across all evaluated** | **{avg:+.1f}%** |",
    ])


def build_calibration() -> str:
    acc = fetch("/kronos/accuracy")
    overall = need(acc, "data", "overall")
    buckets = need(acc, "data", "buckets")
    if not buckets:
        raise RefreshError("kronos accuracy returned no buckets")

    n_total = need(overall, "n_total")
    lookback = need(overall, "lookback_days")
    headline = need(overall, "hit_rate_4d")

    rows = ["| Model confidence | 4-day directional hit rate | Sample |", "|---|---|---|"]
    # Emphasise the highest-confidence bucket — the row that carries the point.
    top = max(buckets, key=lambda b: _low(b["bucket"]))
    for b in buckets:
        label = b["bucket"]
        emph = "**" if b is top else ""
        rows.append(
            f"| {emph}{label}{emph} | {emph}{b['hit_rate_4d']:.1%}{emph} | {b['n_total']:,} |"
        )

    rows.append("")
    rows.append(
        f"*{n_total:,} scored forecasts over {lookback} days. "
        f"Headline hit rate: {headline:.1%}.*"
    )
    return "\n".join(rows)


def _low(bucket_label: str) -> float:
    """Sort key: the lower bound of a '0.8–1.0' style bucket label."""
    m = re.match(r"\s*([0-9.]+)", bucket_label)
    return float(m.group(1)) if m else 0.0


def build_market() -> str:
    g = fetch("/market/global")
    data = need(g, "data")
    assets = need(data, "assets_count")
    oi = need(data, "total_oi")
    qualified = need(data, "qualified_traders")
    tracked = need(data, "tracked_traders")

    return (
        f"**{assets} live markets** · **${oi / 1e9:,.1f}B** open interest · "
        f"**{qualified:,}** quality-scored traders tracked of {tracked:,}"
    )


BLOCKS = {
    "record": build_record,
    "calibration": build_calibration,
    "market": build_market,
}


# ── marker substitution ────────────────────────────────────────────────────

def replace_block(text: str, name: str, body: str) -> str:
    pattern = re.compile(
        rf"(<!-- LIVE:{re.escape(name)} -->)(.*?)(<!-- /LIVE:{re.escape(name)} -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise RefreshError(f"marker <!-- LIVE:{name} --> not found in README.md")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the README is out of date; write nothing")
    args = ap.parse_args()

    original = README.read_text(encoding="utf-8")
    updated = original

    # Build every block BEFORE writing anything. A partial refresh that half
    # succeeds would publish a README whose sections disagree about their date.
    bodies = {}
    for name, builder in BLOCKS.items():
        bodies[name] = builder()

    for name, body in bodies.items():
        updated = replace_block(updated, name, body)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    updated = re.sub(
        r"(<!-- LIVE:stamp -->)(.*?)(<!-- /LIVE:stamp -->)",
        lambda m: f"{m.group(1)}{stamp}{m.group(3)}",
        updated,
        flags=re.DOTALL,
    )

    if updated == original:
        print("README.md already current — no change.")
        return 0

    if args.check:
        print("README.md is STALE — run scripts/refresh_live_numbers.py", file=sys.stderr)
        return 1

    README.write_text(updated, encoding="utf-8")
    print(f"README.md refreshed ({stamp}).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RefreshError as exc:
        # Deliberately loud, deliberately non-writing.
        print(f"refresh FAILED, README left untouched: {exc}", file=sys.stderr)
        raise SystemExit(2)
