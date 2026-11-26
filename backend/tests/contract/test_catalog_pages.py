"""Cursor pagination and bounded crawl tests (US1)."""

from __future__ import annotations

from uaicp.catalog.client import HFClient, Page
from uaicp.catalog.crawler import run_crawl
from uaicp.catalog.report import inventory_report


def _space(i: int) -> dict:
    return {
        "id": f"owner/space-{i}",
        "author": "owner",
        "sdk": "gradio" if i % 2 == 0 else "docker",
        "tags": ["gradio"] + (["mcp-server"] if i % 5 == 0 else []),
        "likes": i,
        "trendingScore": float(i),
        "sha": f"sha-{i}",
        "cardData": {"title": f"Space {i}", "license": "mit" if i % 3 == 0 else None},
        "lastModified": "2026-11-26T00:00:00.000Z",
    }


def test_cursor_pagination_stops_at_limit(session):
    calls = []

    def fetcher(url: str) -> Page:
        calls.append(url)
        page_no = len(calls)
        items = [_space(i) for i in range((page_no - 1) * 2, page_no * 2)]
        cursor = f"cursor-{page_no}" if page_no < 3 else None
        return Page(items=items, next_cursor=cursor)

    client = HFClient(fetcher=fetcher, sleep=lambda _s: None)
    result = run_crawl(session, client, limit=5, page_size=2)
    assert result["created"] == 5
    assert len(calls) == 3
    assert inventory_report(session)["total"] == 5


def test_resume_starts_from_checkpoint_cursor(session):
    calls = []

    def fetcher(url: str) -> Page:
        calls.append(url)
        return Page(items=[_space(len(calls))], next_cursor="done")

    client = HFClient(fetcher=fetcher, sleep=lambda _s: None)
    run_crawl(session, client, limit=1, page_size=1)
    run_crawl(session, client, limit=1, page_size=1)
    assert "cursor=done" in calls[-1]