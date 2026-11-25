"""Unit tests for evidence marks and VERIFY gates (FR-008, FR-009)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from uaicp.domain.enums import EvidenceMark
from uaicp.domain.provenance import (
    Claim,
    Provenance,
    ProvenanceError,
    validate_evidence,
)


def test_no_provenance_is_rejected():
    with pytest.raises(ProvenanceError):
        validate_evidence(EvidenceMark.MEASURED, None)  # type: ignore[arg-type]


def test_reported_requires_url_and_date():
    prov = Provenance(source="hf", source_url=None, observed_at=None)
    with pytest.raises(ProvenanceError):
        validate_evidence(EvidenceMark.REPORTED, prov)

    prov2 = Provenance(
        source="hf",
        source_url="https://example.org",
        observed_at=datetime.now(UTC),
    )
    validate_evidence(EvidenceMark.REPORTED, prov2)  # no raise


def test_verify_must_be_inferred():
    prov = Provenance(source="hf")
    with pytest.raises(ProvenanceError):
        validate_evidence(EvidenceMark.MEASURED, prov, is_verify=True)
    validate_evidence(EvidenceMark.INFERRED, prov, is_verify=True)  # no raise


def test_claim_validate_ok():
    claim = Claim(
        subject="s",
        predicate="p",
        object="o",
        mark=EvidenceMark.MEASURED,
        provenance=Provenance(source="platform"),
    )
    claim.validate()  # no raise