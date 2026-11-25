"""Auto health check: ruff + mypy + pytest, exit non-zero on any failure.

Run from backend/:  python scripts/health.py
"""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PYTHONPATH", os.path.join(ROOT, "src"))

CHECKS = [
    ("ruff", [sys.executable, "-m", "ruff", "check", "src", "tests", "migrations"]),
    ("mypy", [sys.executable, "-m", "mypy", "src"]),
    ("pytest", [sys.executable, "-m", "pytest", "-q"]),
]


def main() -> int:
    failed = 0
    for name, cmd in CHECKS:
        print(f"== {name} ==")
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            failed += 1
            print(f"[FAIL] {name}")
        else:
            print(f"[ OK ] {name}")
    print("\nHEALTH:", "PASS" if failed == 0 else f"FAIL ({failed} checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())