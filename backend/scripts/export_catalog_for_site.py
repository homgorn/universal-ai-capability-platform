"""Backfill categories and export the canonical catalog for the Astro site."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from uaicp.catalog.embed import embed_info

from uaicp.catalog.taxonomy import categorize
from uaicp.db.models import HFSpace
from uaicp.db.session import engine, session_scope

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "site" / "src" / "data"
PUBLIC = ROOT / "site" / "public"


def _summary(row: HFSpace, category: str) -> str:
    author = row.author or "unknown author"
    sdk = row.sdk or "unspecified SDK"
    likes = row.likes if row.likes is not None else 0
    license_text = row.license or "not declared"
    return (
        f"{row.title or row.id} is a {sdk} Space by {author} in {category}, "
        f"with {likes} likes. License: {license_text}."
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)

    with session_scope(engine) as session:
        rows = list(session.query(HFSpace).all())
        records = []
        for row in rows:
            tags = [t for t in (row.tags or []) if not str(t).startswith("region:")]
            category = categorize(tags)
            if row.category != category:
                row.category = category
            embed = embed_info({
                "id": row.id,
                "private": False,
                "subdomain": row.subdomain,
                "sdk": row.sdk,
                "runtime": row.runtime,
            })
            records.append({
                "id": row.id,
                "title": row.title or row.id,
                "author": row.author,
                "sdk": row.sdk or "unknown",
                "category": category,
                "tags": tags,
                "likes": row.likes or 0,
                "trending": int(row.trending_score or 0),
                "license": row.license or "unknown",
                "subdomain": row.subdomain,
                "embed_url": embed.embed_url,
                "embed_status": embed.status,
                "web_component": embed.web_component,
                "embed_reason": embed.reason,
                "sha": row.sha,
                "lastModified": row.last_modified_hf,
                "models": row.models or [],
                "datasets": row.datasets or [],
                "source_url": row.source_url,
                "summary": _summary(row, category),
            })
        records.sort(key=lambda r: (-r["likes"], r["id"]))

    (DATA / "catalog.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Machine-readable catalog endpoints (same canonical inventory).
    api = PUBLIC / "api"
    api.mkdir(parents=True, exist_ok=True)
    well_known = PUBLIC / ".well-known"
    well_known.mkdir(parents=True, exist_ok=True)
    base = "https://uacp-site.rvcdax.workers.dev"
    index_payload = {
        "schema_version": "1.0",
        "updated_utc": datetime.now(UTC).isoformat(),
        "count": len(records),
        "endpoints": [
            "/api/items.json", "/api/index.json", "/api/stats.json",
            "/api/corpus.jsonl", "/catalog-index.json",
        ],
    }
    (api / "index.json").write_text(json.dumps(index_payload, ensure_ascii=False), encoding="utf-8")
    items_payload = {"schema_version": "1.0", "items": records}
    (api / "items.json").write_text(
        json.dumps(items_payload, ensure_ascii=False), encoding="utf-8"
    )
    (api / "stats.json").write_text(
        json.dumps(index_payload, ensure_ascii=False), encoding="utf-8"
    )
    (api / "corpus.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8"
    )
    items_dir = api / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        slug = record["id"].replace("/", "__")
        payload = {"schema_version": "1.0", "item": record}
        (items_dir / f"{slug}.json").write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
    (well_known / "ai-catalog.json").write_text(
        json.dumps({
            "schema_version": "1.0",
            "name": "Universal AI Capability Platform — HF Space catalog",
            "canonical_url": f"{base}/spaces/",
            "endpoints": {
                "index": f"{base}/api/index.json",
                "items": f"{base}/api/items.json",
                "stats": f"{base}/api/stats.json",
                "corpus": f"{base}/api/corpus.jsonl",
            },
        }, ensure_ascii=False), encoding="utf-8"
    )
    (PUBLIC / "catalog-index.json").write_text(
        json.dumps(records, ensure_ascii=False), encoding="utf-8"
    )
    print(f"exported {len(records)} spaces into site catalog")


if __name__ == "__main__":
    main()