"""Store artifact bytes + registry metadata; never inline binaries."""

from __future__ import annotations

from sqlalchemy.orm import Session

from uaicp.db.models import Artifact
from uaicp.domain.enums import DataClass
from uaicp.storage.base import ArtifactStore, verify_hash


def store_artifact(
    session: Session,
    store: ArtifactStore,
    tenant_id: str,
    *,
    key: str,
    data: bytes,
    mime: str,
    artifact_type: str,
    max_bytes: int = 10_000_000,
    classification: DataClass = DataClass.INTERNAL,
) -> Artifact:
    stored = store.put(key, data, mime, max_bytes)
    row = Artifact(
        tenant_id=tenant_id,
        type=artifact_type,
        mime=mime,
        size=stored.size,
        hash=stored.hash,
        storage_uri=stored.storage_uri,
        classification=classification,
    )
    session.add(row)
    session.flush()
    return row


def read_artifact(session: Session, store: ArtifactStore, artifact: Artifact) -> bytes:
    data = store.get(artifact.storage_uri)
    if not verify_hash(data, artifact.hash):
        raise ValueError("ARTIFACT_UNSAFE: hash mismatch")
    return data