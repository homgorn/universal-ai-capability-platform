"""HF Hub client: cursor pagination, rate-limit handling, dead letters."""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlparse

import httpx

_LINK_NEXT = re.compile(r'<([^>]+)>;\s*rel="next"')


class DeadLetter(Exception):
    pass


@dataclass
class Page:
    items: list[dict]
    next_cursor: str | None = None
    headers: dict = field(default_factory=dict)


Fetcher = Callable[[str], Page]


def parse_next_cursor(link_header: str | None) -> str | None:
    if not link_header:
        return None
    match = _LINK_NEXT.search(link_header)
    if not match:
        return None
    query = parse_qs(urlparse(match.group(1)).query)
    return query.get("cursor", [None])[0]


def default_fetcher(url: str) -> Page:
    response = httpx.get(url, timeout=30.0, headers={"User-Agent": "uacp-catalog/0.1"})
    if response.status_code == 429:
        retry_after = float(response.headers.get("retry-after", "1"))
        raise RateLimited(retry_after)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise DeadLetter("unexpected upstream shape: expected list")
    return Page(items=data, next_cursor=parse_next_cursor(response.headers.get("link")))


class RateLimited(Exception):
    def __init__(self, retry_after: float) -> None:
        super().__init__("rate limited")
        self.retry_after = retry_after


class HFClient:
    def __init__(
        self,
        fetcher: Fetcher | None = None,
        sleep=None,
        max_attempts: int = 4,
        base_delay: float = 0.5,
    ) -> None:
        self.fetcher = fetcher or default_fetcher
        self.sleep = sleep or time.sleep
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.dead_letters: list[dict] = []

    def build_url(self, cursor: str | None, limit: int) -> str:
        fields = [
            "author", "cardData", "createdAt", "lastModified", "likes", "models",
            "datasets", "runtime", "sdk", "sha", "subdomain", "tags", "trendingScore",
        ]
        expand = "".join(f"&expand[]={field}" for field in fields)
        url = f"https://huggingface.co/api/spaces?limit={limit}&full=true{expand}"
        if cursor:
            url += f"&cursor={cursor}"
        return url

    def fetch_page(self, cursor: str | None, limit: int = 100) -> Page:
        url = self.build_url(cursor, limit)
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self.fetcher(url)
            except RateLimited as exc:
                delay = max(exc.retry_after, self.base_delay * (2 ** (attempt - 1)))
                self.sleep(min(delay, 60.0))
            except Exception as exc:
                self.dead_letters.append({"url": url, "error": str(exc)})
                raise
        error = f"rate limited after {self.max_attempts} attempts: {url}"
        self.dead_letters.append({"url": url, "error": error})
        raise RateLimited(0)