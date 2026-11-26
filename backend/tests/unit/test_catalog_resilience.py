"""Rate-limit backoff and dead-letter tests (US4)."""

from __future__ import annotations

import pytest

from uaicp.catalog.client import HFClient, Page, RateLimited


def test_429_is_retried_with_backoff():
    sleeps = []
    calls = {"n": 0}

    def fetcher(_u):
        calls["n"] += 1
        if calls["n"] < 3:
            raise RateLimited(0.01)
        return Page(items=[{"id": "x/y"}])

    client = HFClient(fetcher=fetcher, sleep=sleeps.append)
    page = client.fetch_page(None, 10)
    assert page.items == [{"id": "x/y"}]
    assert calls["n"] == 3 and len(sleeps) == 2


def test_bad_payload_is_dead_lettered():
    def fetcher(_u):
        raise ValueError("bad json")

    client = HFClient(fetcher=fetcher, sleep=lambda _s: None)
    with pytest.raises(ValueError):
        client.fetch_page(None, 10)
    assert len(client.dead_letters) == 1


def test_exhausted_retries_are_dead_lettered():
    client = HFClient(fetcher=lambda _u: (_ for _ in ()).throw(RateLimited(0)), sleep=lambda _s: None, max_attempts=2)
    with pytest.raises(RateLimited):
        client.fetch_page(None, 10)
    assert len(client.dead_letters) == 1