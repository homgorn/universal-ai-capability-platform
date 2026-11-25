"""Contract tests for the LLM knowledge surface (contracts/knowledge-surface.md, SC-001)."""

from __future__ import annotations

from uaicp.wiki.corpus import TOPICS
from uaicp.wiki.generate import generate


def test_llms_txt_is_answer_first(tmp_path):
    result = generate(tmp_path)
    text = (tmp_path / "llms.txt").read_text(encoding="utf-8")
    lines = text.splitlines()

    assert lines[0].startswith("# ")
    # first content after H1 is a blockquote summary
    first_quote = next(line for line in lines if line.startswith("> "))
    summary = first_quote[2:].strip()
    assert 40 <= len(summary.split()) <= 120  # 40-80 words target, allow margin

    assert "## Sections" in text
    assert "## Invariants" in text
    assert "## Evidence" in text
    assert result["content_hash"] in text


def test_pages_exist_and_have_sources(tmp_path):
    generate(tmp_path)
    for topic in TOPICS:
        page = tmp_path / "pages" / f"{topic['slug']}.md"
        assert page.exists()
        body = page.read_text(encoding="utf-8")
        assert body.startswith("# ")
        assert "## Sources" in body


def test_verify_topic_lists_unknowns(tmp_path):
    generate(tmp_path)
    verify_page = (tmp_path / "pages" / "verify.md").read_text(encoding="utf-8")
    assert "## VERIFY" in verify_page
    assert "VERIFY" in verify_page


def test_no_fabricated_facts(tmp_path):
    """SC-001: 0 fabricated facts; 100% of topics carry sources."""
    generate(tmp_path)
    for topic in TOPICS:
        page = (tmp_path / "pages" / f"{topic['slug']}.md").read_text(encoding="utf-8")
        assert "## Sources" in page, topic["slug"]
        assert topic["sources"], topic["slug"]
    # Unknowns are surfaced as VERIFY, not asserted as facts.
    assert "VERIFY" in (tmp_path / "pages" / "verify.md").read_text(encoding="utf-8")