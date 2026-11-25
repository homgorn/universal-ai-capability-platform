"""SSRF and dead-letter security tests (FR-008)."""

from __future__ import annotations

import pytest

from uaicp.ingestion.deadletter import is_private_url
from uaicp.ingestion.hf import DiscoveryError, HFAdapter


def test_private_urls_are_denied():
    for url in ("http://127.0.0.1/x", "http://localhost/x", "http://10.0.0.5/x", "http://foo.local/x"):
        assert is_private_url(url), url
    assert not is_private_url("https://huggingface.co/api/spaces")


def test_adapter_rejects_private_resource():
    adapter = HFAdapter(lambda _u: {})
    with pytest.raises(DiscoveryError):
        adapter.ingest_resource("http://127.0.0.1/admin")