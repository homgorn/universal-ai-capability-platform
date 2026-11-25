"""Bounded retries and recorded fallback attempts (SPECS.md §9)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy.orm import Session

from uaicp.db.models import Execution
from uaicp.execution.gateway import record_attempt
from uaicp.validation.errors import ErrorCode

TRANSIENT = {
    ErrorCode.RATE_LIMITED,
    ErrorCode.PROVIDER_UNAVAILABLE,
    ErrorCode.PROVIDER_TIMEOUT,
}


class ProviderCallError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass
class RunResult:
    success: bool
    attempts: int
    value: object | None = None
    error_code: ErrorCode | None = None


def run_with_retry(
    session: Session,
    execution: Execution,
    call: Callable[[], object],
    *,
    max_attempts: int = 3,
    fallback: Callable[[], object] | None = None,
    fallback_reason: str = "primary failed",
) -> RunResult:
    """Run call with bounded retries; fallback is a distinct recorded attempt."""
    for attempt_no in range(1, max_attempts + 1):
        try:
            value = call()
        except ProviderCallError as exc:
            record_attempt(
                session,
                execution,
                attempt_no=attempt_no,
                status="FAILED",
                error_code=exc.code,
            )
            if exc.code not in TRANSIENT:
                return RunResult(False, attempt_no, error_code=exc.code)
            continue
        record_attempt(session, execution, attempt_no=attempt_no, status="SUCCEEDED")
        return RunResult(True, attempt_no, value)

    if fallback is not None:
        record_attempt(
            session,
            execution,
            attempt_no=max_attempts + 1,
            status="FALLBACK",
            reason=fallback_reason,
        )
        try:
            value = fallback()
        except ProviderCallError as exc:
            return RunResult(False, max_attempts + 1, error_code=exc.code)
        return RunResult(True, max_attempts + 1, value)

    return RunResult(False, max_attempts, error_code=ErrorCode.EXECUTION_FAILED)