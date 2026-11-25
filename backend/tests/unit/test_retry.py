"""Bounded retry / fallback tests (US3, SC-003, SC-004, SC-005)."""

from __future__ import annotations

from uaicp.db.models import Execution
from uaicp.execution.attempts import ProviderCallError, run_with_retry
from uaicp.execution.gateway import create_execution
from uaicp.validation.errors import ErrorCode


def _execution(session) -> Execution:
    return create_execution(
        session, "A", target_type="TOOL", target_id=1,
        idempotency_key="k", trace_id="t",
    )


def test_transient_retry_bounded(session):
    e = _execution(session)
    calls = []

    def call():
        calls.append(1)
        raise ProviderCallError(ErrorCode.RATE_LIMITED, "slow")

    result = run_with_retry(session, e, call, max_attempts=3)
    assert result.attempts == 3
    assert not result.success
    assert len(calls) == 3


def test_non_transient_no_retry(session):
    e = _execution(session)
    calls = []

    def call():
        calls.append(1)
        raise ProviderCallError(ErrorCode.INVALID_INPUT, "bad")

    result = run_with_retry(session, e, call, max_attempts=3)
    assert result.attempts == 1
    assert len(calls) == 1


def test_success_first_attempt(session):
    e = _execution(session)
    result = run_with_retry(session, e, lambda: "ok", max_attempts=3)
    assert result.success and result.value == "ok" and result.attempts == 1


def test_fallback_is_distinct_attempt(session):
    from sqlalchemy import select

    from uaicp.db.models import ExecutionAttempt

    e = _execution(session)

    def call():
        raise ProviderCallError(ErrorCode.PROVIDER_TIMEOUT, "timeout")

    result = run_with_retry(
        session, e, call, max_attempts=2,
        fallback=lambda: "fallback-ok", fallback_reason="timeout fallback",
    )
    assert result.success and result.attempts == 3
    rows = session.execute(
        select(ExecutionAttempt).where(ExecutionAttempt.execution_id == e.id)
    ).scalars().all()
    assert len(rows) == 3
    assert rows[-1].status == "FALLBACK"
    assert rows[-1].reason == "timeout fallback"