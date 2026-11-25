"""Live HF Hub verification (measured facts; upstream content is data, never instructions).

Run from backend/:  PYTHONPATH=src python scripts/verify_hf_live.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import httpx

from uaicp.ingestion.hf import HFAdapter, RateLimited


def fetcher(url: str) -> dict:
    response = httpx.get(
        url,
        timeout=15.0,
        headers={"User-Agent": "uacp-live-verify/0.1"},
    )
    if response.status_code == 429:
        raise RateLimited("429")
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        return {"items": data}
    if isinstance(data, dict):
        return data
    raise ValueError("unexpected upstream shape")


def main() -> None:
    adapter = HFAdapter(fetcher)
    items, pages = adapter.discover("background-remover", limit=3, page_size=3)
    sample = adapter.ingest_resource(items[0]["id"]) if items else None

    result = {
        "measured_at": datetime.now(UTC).isoformat(),
        "source": "https://huggingface.co/api/spaces",
        "query": "background-remover",
        "pages_fetched": pages,
        "items": [
            {
                "id": item.get("id"),
                "sdk": item.get("sdk"),
                "private": item.get("private"),
                "tags": item.get("tags", [])[:5],
            }
            for item in items
        ],
        "sample_snapshot": {
            "status": sample.status if sample else None,
            "source_url": sample.snapshot.source_url if sample else None,
            "source_revision": sample.snapshot.source_revision if sample else None,
            "observed_at": sample.snapshot.observed_at.isoformat() if sample else None,
        } if sample else None,
        "verify": [
            "license / redistribution state: not asserted (VERIFY)",
            "exact API limits and quotas: not asserted (VERIFY)",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()