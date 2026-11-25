"""Events and artifacts integration tests (US4, FR-007/FR-008)."""

from __future__ import annotations

from sqlalchemy import select

from uaicp.db.models import ArtifactRef, ExecutionEvent
from uaicp.domain.enums import DataClass, Decision
from uaicp.execution.gateway import add_artifact, apply_policy, create_execution


def test_events_record_transitions(session):
    e = create_execution(
        session, "A", target_type="TOOL", target_id=1,
        idempotency_key="k", trace_id="t",
    )
    apply_policy(session, e, Decision.ALLOW)
    events = session.execute(
        select(ExecutionEvent).where(ExecutionEvent.execution_id == e.id)
    ).scalars().all()
    kinds = [ev.event_type for ev in events]
    assert "created" in kinds and "state" in kinds


def test_artifact_is_reference_only(session):
    e = create_execution(
        session, "A", target_type="TOOL", target_id=1,
        idempotency_key="k", trace_id="t",
    )
    ref = add_artifact(
        session, e, artifact_type="image", mime="image/png", size=1024,
        hash="sha256:abc", storage_uri="s3://bucket/key.png",
        classification=DataClass.INTERNAL,
    )
    assert ref.storage_uri == "s3://bucket/key.png"
    assert session.execute(
        select(ArtifactRef).where(ArtifactRef.execution_id == e.id)
    ).scalar_one() is not None