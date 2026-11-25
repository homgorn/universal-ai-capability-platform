"""Deterministic rendering of the LLM wiki (answer-first, bilingual)."""

from __future__ import annotations

import hashlib
import json


def content_hash(topics: list[dict]) -> str:
    payload = json.dumps(topics, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _sorted(topics: list[dict]) -> list[dict]:
    return sorted(topics, key=lambda t: t["slug"])


def render_llms_txt(topics: list[dict], digest: str) -> str:
    topics = _sorted(topics)
    overview = next(t for t in topics if t["slug"] == "overview")
    lines: list[str] = []
    lines.append(f"# {overview['title_en']}")
    lines.append("")
    lines.append(f"> {overview['answer_en']}")
    lines.append("")
    lines.append(f"**RU:** {overview['answer_ru']}")
    lines.append("")
    lines.append("## Sections")
    lines.append("")
    for t in topics:
        if t["slug"] == "overview":
            continue
        lines.append(f"- [{t['title_en']}](pages/{t['slug']}.md): {t['answer_en'][:120].rstrip()}...")
    lines.append("")
    lines.append("## Invariants")
    lines.append("")
    inv = next(t for t in topics if t["slug"] == "invariants")
    for _, text in inv["table"]["rows"]:
        lines.append(f"- {text}")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    lines.append(
        "Marks: MEASURED (observed directly), REPORTED (external source, URL + date), "
        "INFERRED (derived, surfaced as VERIFY). Unknown values are VERIFY items, never facts."
    )
    lines.append("")
    lines.append(f"content_hash: {digest}")
    lines.append("")
    return "\n".join(lines)


def render_page(topic: dict) -> str:
    lines: list[str] = []
    lines.append(f"# {topic['title_en']}")
    lines.append("")
    lines.append(topic["answer_en"])
    lines.append("")
    lines.append(f"**RU:** {topic['answer_ru']}")
    lines.append("")
    if topic.get("bullets"):
        lines.append("## Key Facts")
        lines.append("")
        for term, definition in topic["bullets"]:
            lines.append(f"- **{term}**: {definition}")
        lines.append("")
    if topic.get("table"):
        lines.append("## Table")
        lines.append("")
        lines.append("| " + " | ".join(topic["table"]["headers"]) + " |")
        lines.append("|" + "|".join(["---"] * len(topic["table"]["headers"])) + "|")
        for row in topic["table"]["rows"]:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")
        lines.append("")
    if topic.get("sources"):
        lines.append("## Sources")
        lines.append("")
        for s in topic["sources"]:
            lines.append(f"- {s}")
        lines.append("")
    if topic.get("verify"):
        lines.append("## VERIFY")
        lines.append("")
        for v in topic["verify"]:
            lines.append(f"- {v}")
        lines.append("")
    return "\n".join(lines)


def render_llms_full(topics: list[dict], digest: str) -> str:
    topics = _sorted(topics)
    parts = ["# Universal AI Capability Platform — Full Knowledge Base", ""]
    parts.append(f"content_hash: {digest}")
    parts.append("")
    for t in topics:
        parts.append(render_page(t))
        parts.append("")
    return "\n".join(parts)