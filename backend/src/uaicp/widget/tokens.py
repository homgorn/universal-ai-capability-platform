"""Scoped, short-lived widget session tokens (SPECS.md §15).

Tokens are stateless HMAC-signed payloads. They carry tenant, tool, channel and
expiry — never provider secrets.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass

_SECRET = os.getenv("WIDGET_TOKEN_SECRET", "dev-only-change-me").encode("utf-8")
DEFAULT_TTL = 300


class TokenError(ValueError):
    pass


@dataclass(frozen=True)
class ScopedToken:
    tenant_id: str
    tool_id: str
    channel: str
    exp: int

    def to_dict(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "tool_id": self.tool_id,
            "channel": self.channel,
            "exp": self.exp,
        }


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def mint(tenant_id: str, tool_id: str, channel: str, ttl: int = DEFAULT_TTL) -> str:
    payload = ScopedToken(tenant_id, tool_id, channel, int(time.time()) + ttl)
    body = _b64(json.dumps(payload.to_dict(), sort_keys=True).encode("utf-8"))
    sig = hmac.new(_SECRET, body.encode("ascii"), hashlib.sha256).digest()
    return f"{body}.{_b64(sig)}"


def verify(token: str, *, now: int | None = None) -> ScopedToken:
    try:
        body, sig = token.split(".", 1)
    except ValueError as exc:
        raise TokenError("malformed token") from exc
    expected = hmac.new(_SECRET, body.encode("ascii"), hashlib.sha256).digest()
    if not hmac.compare_digest(_unb64(sig), expected):
        raise TokenError("bad signature")
    data = json.loads(_unb64(body))
    payload = ScopedToken(
        tenant_id=data["tenant_id"],
        tool_id=data["tool_id"],
        channel=data["channel"],
        exp=int(data["exp"]),
    )
    if (now if now is not None else int(time.time())) >= payload.exp:
        raise TokenError("expired")
    return payload