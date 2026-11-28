"""Mode resolution tests (US3)."""

from __future__ import annotations

import pytest

from uaicp.widget.runtime import open_session, resume_session


def test_modes_resolve_to_execution_api():
    for mode in ("iframe", "web_component", "js_sdk", "direct_api"):
        session = open_session("t", "tool:1", "web", mode)
        assert session.execution_api == "/v1/executions"
        assert session.mode == mode


def test_channel_constraint_denies_before_execution():
    with pytest.raises(PermissionError):
        open_session("t", "tool:1", "telegram", "iframe", payload_bytes=9_000_000)


def test_resume_returns_scoped_token():
    session = open_session("t", "tool:1", "web", "iframe")
    payload = resume_session(session.token)
    assert payload.tool_id == "tool:1"