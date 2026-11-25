"""Deterministic wiki generator: writes llms.txt, llms-full.txt and topic pages."""

from __future__ import annotations

import os
from pathlib import Path

from uaicp.wiki.corpus import TOPICS
from uaicp.wiki.render import content_hash, render_llms_full, render_llms_txt, render_page


def default_output_dir() -> Path:
    override = os.getenv("WIKI_OUT")
    if override:
        return Path(override)
    # .../backend/src/platform/wiki/generate.py -> repo root is parents[4]
    return Path(__file__).resolve().parents[4] / "wiki"


def generate(output_dir: Path | None = None) -> dict:
    out = output_dir or default_output_dir()
    pages_dir = out / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    digest = content_hash(TOPICS)

    (out / "llms.txt").write_text(render_llms_txt(TOPICS, digest), encoding="utf-8")
    (out / "llms-full.txt").write_text(render_llms_full(TOPICS, digest), encoding="utf-8")
    for topic in sorted(TOPICS, key=lambda t: t["slug"]):
        (pages_dir / f"{topic['slug']}.md").write_text(render_page(topic), encoding="utf-8")

    return {"output_dir": str(out), "content_hash": digest, "pages": len(TOPICS)}


def main() -> None:
    result = generate()
    print(
        f"wiki generated: {result['pages']} pages -> {result['output_dir']} "
        f"(content_hash {result['content_hash'][:12]})"
    )


if __name__ == "__main__":
    main()