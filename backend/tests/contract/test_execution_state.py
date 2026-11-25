"""State machine contract tests (US2, SC-002)."""

from __future__ import annotations

import pytest

from uaicp.db.models import Execution
from uaicp.domain.enums import Decision, ExecutionStatus
from uaicp.execution.events import InvalidTransition
from uaicp.execution.gateway import advance, apply_policy, cancel, create_execution, start


def _execution(session) -> Execution:
    return create_execution(
        session, "A", target_type="TOOL", target_id=1,
        idempotency_key="k", trace_id="t",
    )


def test_policy_allow_reaches_queued(session):
    e = _execution(session)
    assert e.status is ExecutionStatus.CREATED
    apply_policy(session, e, Decision.ALLOW)
    assert e.status is ExecutionStatus.QUEUED


def test_policy_deny_sets_denied(session):
    from uaicp.execution.gateway import PolicyDenied

    e = _execution(session)
    with pytest.raises(PolicyDenied):
        apply_policy(session, e, Decision.DENY)
    assert e.status is ExecutionStatus.DENIED


def test_invalid_transition_rejected(session):
    e = _execution(session)
    with pytest.raises(InvalidTransition):
        advance(session, e, ExecutionStatus.SUCCEEDED)


def test_start_and_cancel(session):
    e = _execution(session)
    apply_policy(session, e, Decision.ALLOW)
    start(session, e)
    assert e.status is ExecutionStatus.RUNNING
    cancel(session, e)
    assert e.status is ExecutionStatus.CANCELLED