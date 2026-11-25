"""Append-only contract versioning (FR-004, SC-004, ADR-002 immutability).

The application never updates or deletes a ContractVersion row. A schema change
inserts a new version with an incremented number and a `supersedes_id` link.
"""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import Capability, ContractVersion


def canonical_fingerprint(inputs: dict, outputs: dict) -> str:
    """Deterministic sha256 over canonical JSON (sorted keys, compact separators)."""
    payload = json.dumps(
        {"inputs": inputs, "outputs": outputs},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def next_version(session: Session, capability_id: int) -> int:
    stmt = select(ContractVersion.version).where(
        ContractVersion.capability_id == capability_id
    )
    versions = [v for v in session.execute(stmt).scalars().all()]
    return (max(versions) + 1) if versions else 1


def append_contract(
    session: Session,
    capability: Capability,
    inputs: dict,
    outputs: dict,
    *,
    parser_version: str = "1",
    normalized_version: str = "1",
) -> ContractVersion:
    """Insert a new immutable contract version; never mutate an existing one."""
    version = next_version(session, capability.id)
    supersedes = session.execute(
        select(ContractVersion)
        .where(ContractVersion.capability_id == capability.id)
        .order_by(ContractVersion.version.desc())
    ).scalars().first()
    row = ContractVersion(
        tenant_id=capability.tenant_id,
        capability_id=capability.id,
        version=version,
        supersedes_id=supersedes.id if supersedes else None,
        inputs=inputs,
        outputs=outputs,
        fingerprint=canonical_fingerprint(inputs, outputs),
        parser_version=parser_version,
        normalized_version=normalized_version,
    )
    session.add(row)
    session.flush()
    return row