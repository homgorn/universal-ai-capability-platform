"""Unit tests for error normalization (US3, FR-005/FR-006)."""

from __future__ import annotations

from uaicp.validation import ErrorCode, from_http_status, normalize


def test_all_15_codes_present():
    assert len(ErrorCode) == 15


def test_429_is_rate_limited_and_retryable():
    err = from_http_status(429, "slow down", "execution")
    assert err.code is ErrorCode.RATE_LIMITED
    assert err.retryable is True


def test_400_is_invalid_input_not_retryable():
    err = from_http_status(400, "bad", "execution")
    assert err.code is ErrorCode.INVALID_INPUT
    assert err.retryable is False


def test_500_is_provider_unavailable_retryable():
    err = from_http_status(503, "down", "execution")
    assert err.code is ErrorCode.PROVIDER_UNAVAILABLE
    assert err.retryable is True


def test_unknown_status_is_internal_error():
    err = from_http_status(418, "teapot", "execution")
    assert err.code is ErrorCode.INTERNAL_ERROR


def test_normalized_error_has_all_required_fields():
    err = normalize(ErrorCode.EXECUTION_FAILED, "boom", "runtime")
    d = err.as_dict()
    for key in ("code", "message", "retryable", "stage", "details"):
        assert key in d