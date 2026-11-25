"""Unit tests for deterministic wiki regeneration (SC-006)."""

from __future__ import annotations

from uaicp.wiki.corpus import TOPICS
from uaicp.wiki.generate import generate
from uaicp.wiki.render import content_hash


def test_content_hash_is_stable():
    assert content_hash(TOPICS) == content_hash(TOPICS)


def test_regeneration_is_byte_identical(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    ra = generate(a)
    rb = generate(b)
    assert ra["content_hash"] == rb["content_hash"]

    for name in ["llms.txt", "llms-full.txt"]:
        assert (a / name).read_bytes() == (b / name).read_bytes()

    for topic in TOPICS:
        slug = topic["slug"]
        assert (a / "pages" / f"{slug}.md").read_bytes() == (
            b / "pages" / f"{slug}.md"
        ).read_bytes()