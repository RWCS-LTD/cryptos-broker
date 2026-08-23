"""
CRYPTOS public API client — https://cryptos.broker

A thin, dependency-free wrapper over the endpoints CRYPTOS serves to anonymous
requests. No API key, no account, no registration.

    from cryptos import CryptosClient
    c = CryptosClient()
    print(c.global_stats()["assets_count"], "live markets")

Standard library only. Python 3.9+.

Every method here maps to one endpoint documented in ../docs/api.md. Endpoints
that require a Pro subscription are deliberately absent — this client covers the
free surface, and a 401/403 from a Pro endpoint is not a bug worth wrapping.

MIT licensed. Not affiliated with HyperLiquid.
"""

from __future__ import annotations

import gzip
import json
import time
import urllib.error
import urllib.request
from typing import Any, Optional

__version__ = "1.0.0"

BASE_URL = "https://cryptos.broker/api"
USER_AGENT = f"cryptos-python/{__version__} (+https://github.com/RWCS-LTD/cryptos-broker)"


class CryptosError(RuntimeError):
    """Raised when the API returns an error or unreadable response."""


class CryptosClient:
    """Client for the free CRYPTOS endpoints.

    Args:
        base_url: Override the API root. Rarely needed.
        timeout:  Per-request timeout in seconds.
        retries:  Retry attempts on transport errors and 5xx responses.
                  Retries back off linearly (1s, 2s, 3s...). Never retries a
                  4xx — a 404 or 403 will not become a 200 on a second try.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = 15.0,
        retries: int = 2,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = max(0, retries)

    # ── transport ──────────────────────────────────────────────────────────

    def _get(self, path: str) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
                # The API gzips responses over 1KB; several of these are large.
                "Accept-Encoding": "gzip",
            },
        )

        last_error: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read()
                    if resp.headers.get("Content-Encoding") == "gzip":
                        raw = gzip.decompress(raw)
                    return json.loads(raw.decode("utf-8"))

            except urllib.error.HTTPError as exc:
                # 4xx is a definitive answer — retrying just wastes the caller's
                # time and hammers a rate limiter that is already unhappy.
                if exc.code < 500:
                    detail = ""
                    try:
                        detail = f" — {exc.read().decode('utf-8', 'replace')[:200]}"
                    except Exception:
                        pass
                    raise CryptosError(f"HTTP {exc.code} for {url}{detail}") from exc
                last_error = exc

            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc

            if attempt < self.retries:
                time.sleep(attempt + 1)

        raise CryptosError(f"request to {url} failed: {last_error}") from last_error

    @staticmethod
    def _unwrap(payload: Any) -> Any:
        """Return the `data` field when the endpoint wraps its response.

        Some endpoints return ``{"data": ..., "meta": {...}}`` and others return
        the object directly. Callers should not have to remember which.
        """
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    # ── market ─────────────────────────────────────────────────────────────

    def health(self) -> dict:
        """API liveness check."""
        return self._get("/health")

    def global_stats(self) -> dict:
        """Exchange-wide totals: open interest, live market count, average
        funding, BTC dominance, tracked and quality-scored trader counts."""
        return self._unwrap(self._get("/market/global"))

    def today(self) -> dict:
        """The free daily digest: biggest movers, funding extremes, macro
        regime and the next macro event.

        Descriptive only — it reports what happened and never ranks setups.
        """
        return self._get("/market/today")

    def overview(self) -> Any:
        """Every live market with price, open interest and funding.

        Delisted markets (zero price and zero OI) are filtered server-side.
        """
        return self._unwrap(self._get("/market/overview"))

    def funding_extremes(self) -> dict:
        """The most crowded longs and shorts by funding rate.

        Anonymous callers receive a truncated list — the response carries
        ``limited: true``. Pro ranks the full set by z-score rather than raw
        rate, which is the version that accounts for each asset's own funding
        distribution.
        """
        return self._unwrap(self._get("/market/funding/extremes"))

    def macro(self) -> dict:
        """Current macro regime — the growth/inflation quadrant classification."""
        return self._unwrap(self._get("/market/macro"))

    # ── bitcoin ────────────────────────────────────────────────────────────

    def btc_cycle(self) -> dict:
        """BTC cycle summary: quality score, zone, cycle age, halving number."""
        return self._get("/cycle/btc/summary")

    def btc_onchain(self) -> Any:
        """Live on-chain Bitcoin data."""
        return self._unwrap(self._get("/market/btc/onchain"))

    def btc_seasonality(self) -> Any:
        """Historical average return for today's calendar date and the days
        that follow, with the sample size behind each figure.

        Always read ``n`` before trusting ``avg_pct`` — a 16-sample average is
        a curiosity, not an edge.
        """
        return self._unwrap(self._get("/market/btc/seasonality/today"))

    # ── track record ───────────────────────────────────────────────────────

    def kronos_accuracy(self) -> dict:
        """Published accuracy of the Kronos AI forecasts.

        Returns ``overall``, ``buckets`` (hit rate by confidence bucket) and
        ``per_asset``. The bucket breakdown is the useful part: it shows
        whether the model's own confidence actually predicts its hit rate.
        """
        return self._unwrap(self._get("/kronos/accuracy"))

    def strategies(self) -> dict:
        """Every listed strategy with full in-sample and out-of-sample metrics
        plus its live forward paper record.

        Includes the underperformers. Publishing only the winners is the thing
        this endpoint exists to not do.

        Pro adds the rule set (``params``), the last signal and its timestamp,
        live status and open positions.
        """
        return self._get("/strategies")

    def lab_record(self) -> dict:
        """Aggregate track record across every strategy ever published:
        counts by state, total forward paper trades, how many evaluated
        strategies are net positive, and the average net result.

        Also carries ``retired_experiments`` — each with the reason it was
        shut off and how many unresolved positions were voided rather than
        resolved from hindsight.
        """
        return self._get("/strategies/lab-record")


__all__ = ["CryptosClient", "CryptosError", "BASE_URL", "__version__"]
