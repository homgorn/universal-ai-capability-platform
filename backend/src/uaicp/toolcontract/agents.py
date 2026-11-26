"""Gradio agents.md parser — source of truth for call mechanics."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime

_URL = re.compile(r"https?://[^\s\"'<>)]+")
_UPLOAD = re.compile(r"\bupload\w*\b|\bfile\s+path\b", re.I)
_AUTH = re.compile(r"\bBearer\b|\bAuthorization\b|\btoken\b|\bAPI key\b", re.I)


@dataclass
class AgentContract:
    source_url: str
    observed_at: datetime
    schema_urls: list[str] = field(default_factory=list)
    call_endpoints: list[str] = field(default_factory=list)
    poll_endpoints: list[str] = field(default_factory=list)
    upload_hints: list[str] = field(default_factory=list)
    auth_hints: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "source_url": self.source_url,
            "observed_at": self.observed_at.isoformat(),
            "schema_urls": self.schema_urls,
            "call_endpoints": self.call_endpoints,
            "poll_endpoints": self.poll_endpoints,
            "upload_hints": self.upload_hints,
            "auth_hints": self.auth_hints,
        }


def parse_agents_md(text: str, source_url: str) -> AgentContract:
    urls = [u.rstrip(".,);") for u in _URL.findall(text)]
    lines = text.splitlines()
    return AgentContract(
        source_url=source_url,
        observed_at=datetime.now(UTC),
        schema_urls=[u for u in urls if "openapi" in u or "/info" in u or "mcp/schema" in u],
        call_endpoints=[u for u in urls if "/call/" in u or "queue/join" in u or "/invoke" in u],
        poll_endpoints=[u for u in urls if "queue/data" in u or "/result" in u or "/event" in u],
        upload_hints=[ln.strip() for ln in lines if _UPLOAD.search(ln)][:10],
        auth_hints=[ln.strip() for ln in lines if _AUTH.search(ln)][:10],
    )