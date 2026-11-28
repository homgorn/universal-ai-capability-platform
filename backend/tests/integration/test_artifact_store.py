"""Artifact store + metadata integration tests (US1, SC-001)."""

from __future__ import annotations

from uaicp.db.models import Artifact
from uaicp.domain.enums import DataClass
from uaicp.storage.base import LocalStore
from uaicp.storage.service import read_artifact, store_artifact


def test_store_writes_metadata_and_uri(session, tmp_path):
    store = LocalStore(tmp_path)
    row = store_artifact(
        session, store, "t", key="a/b.bin", data=b"hello", mime="application/octet-stream",
        artifact_type="blob",
    )
    assert row.storage_uri.startswith("file://")
    assert row.hash.startswith("sha256:")
    assert row.classification is DataClass.INTERNAL
    assert session.get(Artifact, row.id) is not None


def test_read_verifies_hash(session, tmp_path):
    store = LocalStore(tmp_path)
    row = store_artifact(
        session, store, "t", key="a/b.bin", data=b"hello", mime="text/plain", artifact_type="text",
    )
    assert read_artifact(session, store, row) == b"hello"
    # tamper
    (tmp_path / "a/b.bin").write_bytes(b"tampered")
    try:
        read_artifact(session, store, row)
    except ValueError as exc:
        assert "ARTIFACT_UNSAFE" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("hash mismatch not detected")