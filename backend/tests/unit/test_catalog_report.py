"""Measured inventory report tests (US5)."""

from __future__ import annotations

from uaicp.catalog.client import HFClient, Page
from uaicp.catalog.crawler import run_crawl
from uaicp.catalog.report import inventory_report


def test_report_matches_database(session):
    items = [
        {"id": "a/1", "sdk": "gradio", "tags": ["mcp-server"], "cardData": {"license": "mit"}},
        {"id": "a/2", "sdk": "docker", "tags": [], "cardData": {}},
    ]
    client = HFClient(fetcher=lambda _u: Page(items=items), sleep=lambda _s: None)
    run_crawl(session, client, limit=2)
    report = inventory_report(session)

    assert report["total"] == 2
    assert report["sdk_distribution"] == {"gradio": 1, "docker": 1}
    assert report["mcp_server"] == 1
    assert report["license_known"] == 1
    assert report["license_unknown"] == 1