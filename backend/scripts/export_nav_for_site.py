"""Generate site navigation (mega menu + 5x2 footer) from the canonical catalog."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "site" / "src" / "data" / "catalog.json"
OUT = ROOT / "site" / "src" / "data" / "nav.json"
BASE = "https://uacp-site.rvcdax.workers.dev"


def link(label: str, href: str) -> dict:
    return {"label": label, "href": href}


def main() -> None:
    records = json.loads(CATALOG.read_text(encoding="utf-8"))

    def top(n: int, key) -> list[dict]:
        return sorted(records, key=key)[:n]

    categories = sorted({r["category"] for r in records})
    sdks = sorted({r["sdk"] for r in records})
    licenses = sorted({r["license"] for r in records})

    tag_counts: dict[str, int] = {}
    for r in records:
        for t in r["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = [t for t, _ in sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:30]]

    nav = {
        "mega": {
            "categories": [link(c, f"/categories/{c}/") for c in categories],
            "sdks": [link(s, f"/sdk/{s}/") for s in sdks],
            "tags": [link(t, f"/tags/{t}/") for t in top_tags],
            "top": [link(r["title"], f"/space/{r['id']}/") for r in top(7, lambda r: -r["likes"])],
        },
        "footer": [
            {"title": "Categories", "links": [link(c, f"/categories/{c}/") for c in categories[:7]]},
            {"title": "More categories", "links": [link(c, f"/categories/{c}/") for c in categories[7:14]]},
            {"title": "SDKs", "links": [link(s, f"/sdk/{s}/") for s in sdks[:7]]},
            {"title": "Popular tags", "links": [link(t, f"/tags/{t}/") for t in top_tags[:7]]},
            {"title": "More tags", "links": [link(t, f"/tags/{t}/") for t in top_tags[7:14]]},
            {"title": "Licenses", "links": [link(l, f"/spaces/?lic={l}") for l in licenses[:7]]},
            {"title": "Top Spaces", "links": [link(r["title"], f"/space/{r['id']}/") for r in top(7, lambda r: -r["likes"])]},
            {"title": "Trending", "links": [link(r["title"], f"/space/{r['id']}/") for r in top(7, lambda r: -r["trending"])]},
            {"title": "Catalog", "links": [
                link("All Spaces", "/spaces/"),
                link("Embed Spaces", "/embed/"),
                link("JSON catalog", "/api/items.json"),
                link("Stats", "/api/stats.json"),
                link("Categories", "/categories/"),
                link("Machine-readable index", "/.well-known/ai-catalog.json"),
            ]},
            {"title": "Resources", "links": [
                link("Documentation", "/en/docs/"),
                link("Research source", "/en/docs/catalog-crawler/"),
                link("llms.txt", "/llms.txt"),
                link("GitHub", "https://github.com/homgorn/universal-ai-capability-platform"),
                link("Constitution", "https://github.com/homgorn/universal-ai-capability-platform/blob/main/.specify/memory/constitution.md"),
            ]},
        ],
        "base": BASE,
    }
    OUT.write_text(json.dumps(nav, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"navigation generated: {len(nav['mega']['tags'])} mega tags, {len(nav['footer'])} footer groups")


if __name__ == "__main__":
    main()