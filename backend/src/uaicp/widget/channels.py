"""Channel constraint contracts (SPECS.md §15, Correction 12)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChannelConstraints:
    channel: str
    auth: str  # none | session_token | oauth
    file_support: bool
    streaming: bool
    max_payload_bytes: int
    requires_https: bool
    allows_iframe: bool


CHANNELS: dict[str, ChannelConstraints] = {
    "web": ChannelConstraints("web", "session_token", True, True, 10_000_000, True, True),
    "telegram": ChannelConstraints("telegram", "session_token", True, True, 4_000_000, True, False),
    "discord": ChannelConstraints("discord", "oauth", True, False, 8_000_000, True, True),
    "teams": ChannelConstraints("teams", "oauth", True, True, 8_000_000, True, True),
    "line": ChannelConstraints("line", "session_token", True, False, 4_000_000, True, True),
    "api": ChannelConstraints("api", "session_token", True, True, 50_000_000, True, False),
}


def constraints_for(channel: str) -> ChannelConstraints:
    try:
        return CHANNELS[channel]
    except KeyError as exc:
        raise ValueError(f"unknown channel {channel}") from exc


def check_request(
    channel: str,
    *,
    has_file: bool,
    payload_bytes: int,
    streaming: bool,
) -> tuple[bool, str]:
    """Return (allowed, reason). Denials happen before any provider call."""
    c = constraints_for(channel)
    if has_file and not c.file_support:
        return False, f"{channel} does not support files"
    if payload_bytes > c.max_payload_bytes:
        return False, f"{channel} payload exceeds {c.max_payload_bytes} bytes"
    if streaming and not c.streaming:
        return False, f"{channel} does not support streaming"
    return True, ""