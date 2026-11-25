"""Durable execution gateway: idempotency, policy, state machine."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import ArtifactRef, Execution, ExecutionAttempt
from uaicp.domain.enums import Decision, ExecutionStatus
from uaicp.execution.events import record_event, validate_transition
from uaicp.validation.errors import ErrorCode


class PolicyDenied(Exception):
    """Raised when policy denies an execution."""


def create_execution(
    session: Session,
    tenant_id: str,
    *,
    target_type: str,
    target_id: int,
    idempotency_key: str,
    trace_id: str,
    estimated_cost: float | None = None,
) -> Execution:
    """Create an execution, or return the existing one for a duplicate key (US1)."""
    existing = session.execute(
        select(Execution).where(
            Execution.tenant_id == tenant_id,
            Execution.idempotency_key == idempotency_key,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing
    execution = Execution(
        tenant_id=tenant_id,
        target_type=target_type,
        target_id=target_id,
        status=ExecutionStatus.CREATED,
        idempotency_key=idempotency_key,
        trace_id=trace_id,
        estimated_cost=estimated_cost,
    )
    session.add(execution)
    session.flush()
    record_event(session, execution, "created", to_state=ExecutionStatus.CREATED)
    return execution


def advance(
    session: Session,
    execution: Execution,
    target: ExecutionStatus,
    *,
    payload: dict | None = None,
) -> Execution:
    """Validate and apply a state transition, recording an event."""
    validate_transition(execution.status, target)  # type: ignore[arg-type]
    previous = execution.status
    execution.status = target
    record_event(
        session,
        execution,
        "state",
        from_state=previous,  # type: ignore[arg-type]
        to_state=target,
        payload=payload,
    )
    session.flush()
    return execution


def apply_policy(session: Session, execution: Execution, decision: Decision) -> Execution:
    advance(session, execution, ExecutionStatus.POLICY_CHECK)
    if decision in (Decision.DENY,):
        advance(session, execution, ExecutionStatus.DENIED)
        raise PolicyDenied(f"execution {execution.id} denied by policy")
    # ALLOW, ALLOW_WITH_LIMITS, REQUIRE_APPROVAL proceed to queue in this gateway.
    advance(session, execution, ExecutionStatus.QUEUED)
    return execution


def cancel(session: Session, execution: Execution) -> Execution:
    return advance(session, execution, ExecutionStatus.CANCELLED)


def start(session: Session, execution: Execution) -> Execution:
    advance(session, execution, ExecutionStatus.STARTING)
    return advance(session, execution, ExecutionStatus.RUNNING)


def complete(
    session: Session,
    execution: Execution,
    *,
    actual_cost: float | None = None,
) -> Execution:
    execution.actual_cost = actual_cost
    return advance(session, execution, ExecutionStatus.SUCCEEDED)


def record_attempt(
    session: Session,
    execution: Execution,
    *,
    attempt_no: int,
    status: str,
    error_code: ErrorCode | str | None = None,
    reason: str | None = None,
    provider: str | None = None,
) -> ExecutionAttempt:
    attempt = ExecutionAttempt(
        tenant_id=execution.tenant_id,
        execution_id=execution.id,
        attempt_no=attempt_no,
        status=status,
        error_code=error_code.value if isinstance(error_code, ErrorCode) else error_code,
        reason=reason,
        provider=provider,
    )
    session.add(attempt)
    session.flush()
    return attempt


def add_artifact(
    session: Session,
    execution: Execution,
    *,
    artifact_type: str,
    mime: str,
    size: int,
    hash: str,
    storage_uri: str,
    classification,
) -> ArtifactRef:
    ref = ArtifactRef(
        tenant_id=execution.tenant_id,
        execution_id=execution.id,
        artifact_type=artifact_type,
        mime=mime,
        size=size,
        hash=hash,
        storage_uri=storage_uri,
        classification=classification,
    )
    session.add(ref)
    session.flush()
    return ref