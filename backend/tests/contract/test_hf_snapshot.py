"""Raw snapshot + provenance contract tests (US2)."""

from __future__ import annotations

from uaicp.ingestion.hf import HFAdapter


def test_ingest_stores_snapshot_and_provenance():
    payload = {"id": "demo/bg", "sha": "abc123", "private": False}

    def fetcher(_url: str) -> dict:
        return payload

    result = HFAdapter(fetcher).ingest_resource("demo/bg")
    assert result.status == "DISCOVERED"
    assert result.snapshot.payload == payload
    assert result.snapshot.source_revision == "abc123"
    assert result.provenance["source"] == "hf"
    assert result.provenance["raw_snapshot"] == payload
    assert result.provenance["parser_version"] == "1"


def test_ingested_resource_is_never_active():
    result = HFAdapter(lambda _u: {"sha": "x"}).ingest_resource("demo/x")
    assert result.status != "ACTIVE"