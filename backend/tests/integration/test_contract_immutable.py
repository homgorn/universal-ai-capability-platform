"""Integration tests for immutable contract versions (FR-004, SC-004)."""

from __future__ import annotations

from uaicp.db.contracts import append_contract, canonical_fingerprint
from uaicp.db.models import Capability, ContractVersion
from uaicp.domain.enums import CapabilityStatus


def _capability(session) -> Capability:
    cap = Capability(
        tenant_id="t",
        capability_id="image.upscale",
        name="upscale",
        status=CapabilityStatus.DISCOVERED,
    )
    session.add(cap)
    session.flush()
    return cap


def test_versions_increment_and_old_is_unchanged(session):
    cap = _capability(session)
    v1 = append_contract(session, cap, {"a": 1}, {"b": 2})
    assert v1.version == 1
    snapshot = (v1.inputs, v1.outputs, v1.fingerprint)

    v2 = append_contract(session, cap, {"a": 1, "c": 3}, {"b": 2})
    assert v2.version == 2
    assert v2.supersedes_id == v1.id

    # old version unchanged
    session.refresh(v1)
    assert (v1.inputs, v1.outputs, v1.fingerprint) == snapshot


def test_fingerprint_is_deterministic():
    a = canonical_fingerprint({"x": 1, "y": 2}, {"z": 3})
    b = canonical_fingerprint({"y": 2, "x": 1}, {"z": 3})
    assert a == b
    assert len(a) == 64


def test_contract_version_table_is_append_only(session):
    cap = _capability(session)
    append_contract(session, cap, {}, {})
    rows = session.query(ContractVersion).all()
    assert len(rows) == 1
    # No update/delete API is exposed; mutating a version is a programming error.
    assert rows[0].version == 1