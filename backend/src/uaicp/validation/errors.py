"""Normalized error taxonomy (SPECS.md §4) — exactly 15 codes."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    INVALID_INPUT = "INVALID_INPUT"
    CONTRACT_MISMATCH = "CONTRACT_MISMATCH"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    AUTH_FAILED = "AUTH_FAILED"
    POLICY_DENIED = "POLICY_DENIED"
    RATE_LIMITED = "RATE_LIMITED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    PROVIDER_TIMEOUT = "PROVIDER_TIMEOUT"
    SCHEMA_DRIFT = "SCHEMA_DRIFT"
    ARTIFACT_TOO_LARGE = "ARTIFACT_TOO_LARGE"
    ARTIFACT_UNSAFE = "ARTIFACT_UNSAFE"
    EXECUTION_CANCELLED = "EXECUTION_CANCELLED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# Retryable by default for transient conditions.
_RETRYABLE: set[ErrorCode] = {
    ErrorCode.RATE_LIMITED,
    ErrorCode.PROVIDER_UNAVAILABLE,
    ErrorCode.PROVIDER_TIMEOUT,
}


@dataclass
class NormalizedError:
    code: ErrorCode
    message: str
    retryable: bool
    stage: str
    details: dict = field(default_factory=dict)
    retry_after: float | None = None
    provider_error: dict | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code.value,
            "message": self.message,
            "retryable": self.retryable,
            "stage": self.stage,
            "details": self.details,
            "retry_after": self.retry_after,
            "provider_error": self.provider_error,
        }


def normalize(
    code: ErrorCode,
    message: str,
    stage: str,
    *,
    retryable: bool | None = None,
    details: dict | None = None,
    retry_after: float | None = None,
    provider_error: dict | None = None,
) -> NormalizedError:
    if retryable is None:
        retryable = code in _RETRYABLE
    return NormalizedError(
        code=code,
        message=message,
        retryable=retryable,
        stage=stage,
        details=details or {},
        retry_after=retry_after,
        provider_error=provider_error,
    )


_STATUS_MAP: dict[int, ErrorCode] = {
    400: ErrorCode.INVALID_INPUT,
    401: ErrorCode.AUTH_REQUIRED,
    403: ErrorCode.AUTH_FAILED,
    409: ErrorCode.CONTRACT_MISMATCH,
    413: ErrorCode.ARTIFACT_TOO_LARGE,
    429: ErrorCode.RATE_LIMITED,
}


def from_http_status(
    status: int,
    message: str,
    stage: str,
    *,
    provider_error: dict | None = None,
    retry_after: float | None = None,
) -> NormalizedError:
    if status in _STATUS_MAP:
        code = _STATUS_MAP[status]
    elif status == 408:
        code = ErrorCode.PROVIDER_TIMEOUT
    elif 500 <= status < 600:
        code = ErrorCode.PROVIDER_UNAVAILABLE
    else:
        code = ErrorCode.INTERNAL_ERROR
    return normalize(
        code,
        message,
        stage,
        retry_after=retry_after,
        provider_error=provider_error,
    )