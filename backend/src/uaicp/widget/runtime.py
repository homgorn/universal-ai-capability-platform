"""Widget runtime: mode resolution to the Execution API contract."""

from __future__ import annotations

from dataclasses import dataclass

from uaicp.widget.channels import check_request
from uaicp.widget.tokens import ScopedToken, mint, verify

MODES = ("iframe", "web_component", "js_sdk", "direct_api")


@dataclass
class WidgetSession:
    token: str
    mode: str
    execution_api: str
    tool_id: str
    channel: str


def open_session(
    tenant_id: str,
    tool_id: str,
    channel: str,
    mode: str,
    *,
    has_file: bool = False,
    payload_bytes: int = 0,
    streaming: bool = False,
) -> WidgetSession:
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode}")
    allowed, reason = check_request(
        channel, has_file=has_file, payload_bytes=payload_bytes, streaming=streaming
    )
    if not allowed:
        raise PermissionError(reason)
    token = mint(tenant_id, tool_id, channel)
    return WidgetSession(
        token=token,
        mode=mode,
        execution_api="/v1/executions",
        tool_id=tool_id,
        channel=channel,
    )


def resume_session(token: str) -> ScopedToken:
    return verify(token)