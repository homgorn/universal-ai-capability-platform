"""Execution state machine and structured events (SPECS.md §9)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from uaicp.db.models import Execution, ExecutionEvent
from uaicp.domain.enums import ExecutionStatus

ALLOWED: dict[ExecutionStatus, set[ExecutionStatus]] = {
    ExecutionStatus.CREATED: {
        ExecutionStatus.POLICY_CHECK,
        ExecutionStatus.CANCELLED,
        ExecutionStatus.EXPIRED,
    },
    ExecutionStatus.POLICY_CHECK: {ExecutionStatus.QUEUED, ExecutionStatus.DENIED},
    ExecutionStatus.QUEUED: {
        ExecutionStatus.STARTING,
        ExecutionStatus.CANCELLED,
        ExecutionStatus.EXPIRED,
    },
    ExecutionStatus.STARTING: {ExecutionStatus.RUNNING, ExecutionStatus.CANCELLED},
    ExecutionStatus.RUNNING: {
        ExecutionStatus.STREAMING,
        ExecutionStatus.SUCCEEDED,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    },
    ExecutionStatus.STREAMING: {
        ExecutionStatus.SUCCEEDED,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    },
}


class InvalidTransition(ValueError):
    """Raised when an illegal state transition is attempted."""


def validate_transition(current: ExecutionStatus, target: ExecutionStatus) -> None:
    if target not in ALLOWED.get(current, set()):
        raise InvalidTransition(f"{current.value} -> {target.value}")


def record_event(
    session: Session,
    execution: Execution,
    event_type: str,
    *,
    from_state: ExecutionStatus | None = None,
    to_state: ExecutionStatus | None = None,
    payload: dict | None = None,
) -> ExecutionEvent:
    event = ExecutionEvent(
        tenant_id=execution.tenant_id,
        execution_id=execution.id,
        event_type=event_type,
        from_state=from_state.value if from_state else None,
        to_state=to_state.value if to_state else None,
        payload=payload or {},
    )
    session.add(event)
    session.flush()
    return event