"""Scoped token tests (US1, SC-001)."""

from __future__ import annotations

import pytest

from uaicp.widget.tokens import TokenError, mint, verify


def test_token_roundtrip():
    token = mint("tenant-a", "tool:1", "web")
    payload = verify(token)
    assert payload.tenant_id == "tenant-a"
    assert payload.tool_id == "tool:1"
    assert payload.channel == "web"


def test_expired_token_rejected():
    token = mint("t", "tool:1", "web", ttl=0)
    with pytest.raises(TokenError):
        verify(token)


def test_tampered_token_rejected():
    token = mint("t", "tool:1", "web")
    with pytest.raises(TokenError):
        verify(token + "x")


def test_token_has_no_secret_fields():
    token = mint("t", "tool:1", "web")
    assert "secret" not in token.lower()
    assert "api_key" not in token.lower()