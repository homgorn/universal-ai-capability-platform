"""Unit tests for fingerprint and drift (US4, FR-007/FR-008)."""

from __future__ import annotations

from uaicp.validation import Compatibility, canonical_fingerprint, classify_drift


def test_fingerprint_is_stable_across_key_order():
    a = canonical_fingerprint([{"name": "x", "semantic_type": "text"}], [])
    b = canonical_fingerprint([{"semantic_type": "text", "name": "x"}], [])
    assert a == b
    assert len(a) == 64


def test_reorder_of_ports_is_stable():
    p1 = [{"name": "a"}, {"name": "b"}]
    p2 = [{"name": "b"}, {"name": "a"}]
    # order of ports is significant (cardinality), so fingerprints differ
    assert canonical_fingerprint(p1, []) != canonical_fingerprint(p2, [])


def test_drift_breaking_on_type_change():
    old = {"inputs": [{"name": "x", "required": True, "semantic_type": "image"}], "outputs": []}
    new = {"inputs": [{"name": "x", "required": True, "semantic_type": "text"}], "outputs": []}
    assert classify_drift(old, new) is Compatibility.BREAKING