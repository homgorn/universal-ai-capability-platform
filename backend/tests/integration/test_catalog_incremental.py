"""SHA-driven incremental updates (US2)."""

from __future__ import annotations

from uaicp.catalog.client import HFClient, Page
from uaicp.catalog.crawler import run_crawl
from uaicp.db.models import HFSpace


def _space(sha: str) -> dict:
    return {"id": "owner/space", "sha": sha, "sdk": "gradio", "cardData": {"title": "T"}}


def test_unchanged_sha_does_not_create_history(session):
    client = HFClient(fetcher=lambda _u: Page(items=[_space("sha-1")]), sleep=lambda _s: None)
    first = run_crawl(session, client, limit=1)
    second = run_crawl(session, client, limit=1)
    assert first["created"] == 1
    assert second["unchanged"] == 1
    row = session.get(HFSpace, "owner/space")
    assert row.snapshot_history == []
    assert row.times_seen == 2


def test_changed_sha_preserves_old_snapshot(session):
    state = {"sha": "sha-1"}

    def fetcher(_u):
        return Page(items=[_space(state["sha"])])

    client = HFClient(fetcher=fetcher, sleep=lambda _s: None)
    run_crawl(session, client, limit=1)
    state["sha"] = "sha-2"
    result = run_crawl(session, client, limit=1)

    assert result["updated"] == 1
    row = session.get(HFSpace, "owner/space")
    assert row.sha == "sha-2"
    assert len(row.snapshot_history) == 1
    assert row.snapshot_history[0]["sha"] == "sha-1"