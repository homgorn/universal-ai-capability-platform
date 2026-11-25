"""Discovery pagination and backoff tests (US1)."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest

from uaicp.ingestion.hf import HFAdapter, RateLimited, backoff


def _paged_fetcher(url: str) -> dict:
    cursor = parse_qs(urlparse(url).query).get("cursor", [None])[0]
    if cursor is None:
        return {"items": [{"id": i} for i in range(10)], "cursor": "p2"}
    if cursor == "p2":
        return {"items": [{"id": i} for i in range(10, 20)], "cursor": "p3"}
    return {"items": [{"id": i} for i in range(20, 30)], "cursor": None}


def test_pagination_stops_at_limit():
    adapter = HFAdapter(_paged_fetcher)
    items, pages = adapter.discover("bg", limit=25, page_size=10)
    assert len(items) == 25
    assert pages == 3


def test_backoff_is_exponential_and_bounded():
    assert backoff(1) == pytest.approx(0.15)
    assert backoff(2) == pytest.approx(0.25)
    assert backoff(20) <= 2.06


def test_rate_limited_retries_then_succeeds():
    calls = {"n": 0}
    sleeps: list[float] = []

    def fetcher(_url: str) -> dict:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RateLimited("429")
        return {"items": [{"id": 1}]}

    adapter = HFAdapter(fetcher, sleep=sleeps.append)
    items, pages = adapter.discover("x")
    assert items == [{"id": 1}] and pages == 1
    assert calls["n"] == 3
    assert len(sleeps) == 2


def test_dead_letters_on_malformed_upstream():
    def fetcher(_url: str) -> dict:
        raise ValueError("bad json")

    adapter = HFAdapter(fetcher)
    try:
        adapter.discover("x")
    except ValueError:
        pass
    assert len(adapter.dead_letters.list()) == 1