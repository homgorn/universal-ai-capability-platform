"""Verify embed URLs respond (HEAD/GET status) without executing Space code."""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "site" / "src" / "data" / "catalog.json"


def main() -> None:
    records = json.loads(CATALOG.read_text(encoding="utf-8"))
    sample = [r for r in records if r.get("embed_status") == "EMBEDDABLE" and r.get("embed_url")][:25]
    results = []
    with httpx.Client(timeout=10.0, follow_redirects=False, headers={"User-Agent": "uacp-embed-check/0.1"}) as client:
        for r in sample:
            url = r["embed_url"]
            try:
                resp = client.get(url)
                status = resp.status_code
            except Exception as exc:
                status = f"ERR {type(exc).__name__}"
            results.append({"id": r["id"], "url": url, "status": status})
    ok = sum(1 for x in results if isinstance(x["status"], int) and x["status"] < 400)
    print(json.dumps({"checked": len(results), "ok": ok, "results": results}, indent=2, ensure_ascii=False))
    print(f"EMBED CHECK: {ok}/{len(results)} reachable")


if __name__ == "__main__":
    main()