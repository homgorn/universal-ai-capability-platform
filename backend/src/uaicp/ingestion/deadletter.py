"""Dead-letter queue and SSRF guard for discovery (SPECS.md §5, §6)."""

from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

_PRIVATE_HOSTS = {"localhost", "0.0.0.0", "::1"}


def is_private_url(url: str) -> bool:
    """Deny private/loopback/link-local targets by default."""
    host = (urlparse(url).hostname or "").lower()
    if host in _PRIVATE_HOSTS or host.endswith(".local") or host.endswith(".internal"):
        return True
    try:
        return ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


class DeadLetterQueue:
    """In-memory failure record (persistence delegated to the caller in production)."""

    def __init__(self) -> None:
        self._items: list[dict] = []

    def add(self, record: dict) -> None:
        self._items.append(record)

    def list(self) -> list[dict]:
        return list(self._items)
