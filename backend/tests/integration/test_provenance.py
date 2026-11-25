"""Integration tests for mandatory provenance (FR-005, SC-002)."""

from __future__ import annotations

import pytest
from sqlalchemy.exc import IntegrityError

from uaicp.db.models import Resource
from uaicp.domain.enums import EvidenceMark, ResourceType


def test_resource_without_source_is_rejected(session):
    session.add(
        Resource(
            tenant_id="t",
            provider_id=1,
            resource_type=ResourceType.MODEL,
            name="no-source",
            # source intentionally omitted (NOT NULL)
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()


def test_resource_with_provenance_persists(session):
    r = Resource(
        tenant_id="t",
        provider_id=1,
        resource_type=ResourceType.MODEL,
        name="ok",
        source="hf",
        source_url="https://example.org",
        evidence_mark=EvidenceMark.REPORTED,
    )
    session.add(r)
    session.flush()
    assert r.id is not None
    assert r.source == "hf"
    assert r.evidence_mark is EvidenceMark.REPORTED