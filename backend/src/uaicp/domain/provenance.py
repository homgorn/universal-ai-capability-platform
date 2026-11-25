"""Provenance value object and evidence-mark enforcement (SPECS.md §7, constitution IV)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from uaicp.domain.enums import EvidenceMark


class ProvenanceError(ValueError):
    """Raised when a claim lacks required provenance or evidence marking."""


@dataclass(frozen=True)
class Provenance:
    source: str
    source_url: str | None = None
    observed_at: datetime | None = None
    source_revision: str | None = None
    raw_snapshot: dict | None = None
    parser_version: str = "1"
    normalized_version: str = "1"

    def __post_init__(self) -> None:
        if not self.source:
            raise ProvenanceError("source is required")

    def as_dict(self) -> dict:
        return {
            "source": self.source,
            "source_url": self.source_url,
            "observed_at": _iso(self.observed_at),
            "source_revision": self.source_revision,
            "raw_snapshot": self.raw_snapshot,
            "parser_version": self.parser_version,
            "normalized_version": self.normalized_version,
        }


def _iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def validate_evidence(
    mark: EvidenceMark,
    provenance: Provenance,
    *,
    is_verify: bool = False,
) -> None:
    """Enforce FR-008/FR-009: REPORTED needs URL+date; missing provenance is rejected."""
    if provenance is None:
        raise ProvenanceError("provenance is mandatory")
    if mark is EvidenceMark.REPORTED:
        if not provenance.source_url:
            raise ProvenanceError("REPORTED evidence requires source_url")
        if provenance.observed_at is None:
            raise ProvenanceError("REPORTED evidence requires observed_at")
    if is_verify and mark is not EvidenceMark.INFERRED:
        raise ProvenanceError("VERIFY items must be marked INFERRED")


@dataclass
class Claim:
    """A single factual claim with its evidence mark (feeds the wiki + graph)."""

    subject: str
    predicate: str
    object: str
    mark: EvidenceMark
    provenance: Provenance
    is_verify: bool = False
    fields: dict = field(default_factory=dict)

    def validate(self) -> None:
        validate_evidence(self.mark, self.provenance, is_verify=self.is_verify)