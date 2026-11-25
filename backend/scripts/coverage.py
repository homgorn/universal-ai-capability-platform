"""Coverage snapshot: count requirements (FR/SC) and tasks, per user story.

Run from backend/:  python scripts/coverage.py
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "specs" / "001-knowledge-foundation" / "spec.md"
TASKS = ROOT / "specs" / "001-knowledge-foundation" / "tasks.md"


def main() -> None:
    spec = SPEC.read_text(encoding="utf-8")
    tasks = TASKS.read_text(encoding="utf-8")

    fr = sorted(set(re.findall(r"FR-\d{3}", spec)))
    sc = sorted(set(re.findall(r"SC-\d{3}", spec)))
    task_ids = re.findall(r"^- \[.\] (T\d{3})", tasks, flags=re.MULTILINE)

    print(f"Requirements: {len(fr)} FR, {len(sc)} SC")
    print(f"Tasks: {len(task_ids)}")
    print("FR:", ", ".join(fr))
    print("SC:", ", ".join(sc))

    # Per-story task counts
    stories: dict[str, int] = {}
    for line in tasks.splitlines():
        m = re.search(r"\[(US\d+)\]", line)
        if m and line.strip().startswith("- ["):
            stories[m.group(1)] = stories.get(m.group(1), 0) + 1
    print("Tasks per story:", stories)


if __name__ == "__main__":
    main()