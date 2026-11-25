"""HF discovery and ingestion with an injected HTTP transport (never executes resources)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime

from uaicp.ingestion.deadletter import DeadLetterQueue, is_private_url

Fetcher = Callable[[str], dict]
Sleep = Callable[[float], None]


class RateLimited(Exception):
    """Upstream returned 429."""


class DiscoveryError(Exception):
    """Discovery failed after bounded retries."""


@dataclass(frozen=True)
class RawSnapshot:
    source_url: str
    observed_at: datetime
    source_revision: str | None
    payload: dict
    parser_version: str = "1"
    normalized_version: str = "1"


@dataclass
class DiscoveredResource:
    id: str
    snapshot: RawSnapshot
    status: str = "DISCOVERED"
    provenance: dict = field(default_factory=dict)


def backoff(attempt: int, base: float = 0.1, cap: float = 2.0, jitter: float = 0.05) -> float:
    """Exponential backoff with deterministic jitter (bounded by cap)."""
    return min(cap, base * (2 ** (attempt - 1))) + jitter


class HFAdapter:
    """HF source adapter. Discovery only: no provider code is ever executed."""

    def __init__(self, fetcher: Fetcher, sleep: Sleep | None = None) -> None:
        self.fetcher = fetcher
        self.sleep = sleep or (lambda _seconds: None)
        self.dead_letters = DeadLetterQueue()

    def _fetch(self, url: str, max_attempts: int = 3) -> dict:
        if is_private_url(url):
            raise DiscoveryError(f"private-network URL denied: {url}")
        for attempt in range(1, max_attempts + 1):
            try:
                return self.fetcher(url)
            except RateLimited:
                if attempt == max_attempts:
                    break
                self.sleep(backoff(attempt))
            except Exception as exc:  # malformed upstream / transport failure
                self.dead_letters.add({"url": url, "error": str(exc)})
                raise
        error = f"rate limited after {max_attempts} attempts: {url}"
        self.dead_letters.add({"url": url, "error": error})
        raise DiscoveryError(error)

    def discover(self, query: str, limit: int = 25, page_size: int = 10) -> tuple[list[dict], int]:
        """Paginate HF search results; return (items, page_count)."""
        items: list[dict] = []
        cursor: str | None = None
        pages = 0
        while len(items) < limit and pages < 100:
            url = f"https://huggingface.co/api/spaces?search={query}&limit={page_size}"
            if cursor:
                url += f"&cursor={cursor}"
            data = self._fetch(url)
            batch = data.get("items") or data.get("spaces") or []
            if not batch:
                break
            items.extend(batch[: limit - len(items)])
            pages += 1
            cursor = data.get("cursor") or data.get("next")
            if not cursor:
                break
        return items, pages

    def ingest_resource(self, resource_id: str, kind: str = "space") -> DiscoveredResource:
        """Store a raw snapshot + provenance. Status stays DISCOVERED (never executable)."""
        if is_private_url(resource_id):
            raise DiscoveryError(f"private-network resource denied: {resource_id}")
        endpoint = "spaces" if kind == "space" else "models"
        url = f"https://huggingface.co/api/{endpoint}/{resource_id}"
        payload = self._fetch(url)
        revision = payload.get("sha") or payload.get("revision")
        snapshot = RawSnapshot(
            source_url=url,
            observed_at=datetime.now(UTC),
            source_revision=revision,
            payload=payload,
        )
        return DiscoveredResource(
            id=resource_id,
            snapshot=snapshot,
            status="DISCOVERED",
            provenance={
                "source": "hf",
                "source_url": url,
                "observed_at": snapshot.observed_at.isoformat(),
                "source_revision": revision,
                "raw_snapshot": payload,
                "parser_version": snapshot.parser_version,
                "normalized_version": snapshot.normalized_version,
            },
        )