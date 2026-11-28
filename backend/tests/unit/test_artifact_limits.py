"""Artifact limit tests (US3)."""

from __future__ import annotations

import pytest

from uaicp.storage.base import ArtifactTooLarge, LocalStore


def test_oversized_rejected(tmp_path):
    store = LocalStore(tmp_path)
    with pytest.raises(ArtifactTooLarge):
        store.put("k", b"x" * 100, "text/plain", max_bytes=10)


def test_within_limit_ok(tmp_path):
    store = LocalStore(tmp_path)
    stored = store.put("k", b"x" * 10, "text/plain", max_bytes=100)
    assert stored.size == 10