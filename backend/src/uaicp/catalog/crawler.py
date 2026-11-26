"""Crawl orchestration: canonical upsert, SHA-driven updates, resumable checkpoint."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from uaicp.catalog.client import HFClient
from uaicp.db.models import HFSpace, IngestCheckpoint

SOURCE = "hf:spaces"


def canonicalize(raw: dict) -> dict:
    card = raw.get("cardData") or {}
    license_value = card.get("license")
    if isinstance(license_value, dict):
        license_value = license_value.get("name") or license_value.get("id")
    space_id = raw.get("id", "")
    return {
        "author": raw.get("author"),
        "title": card.get("title"),
        "sdk": raw.get("sdk"),
        "tags": raw.get("tags") or [],
        "likes": raw.get("likes"),
        "trending_score": raw.get("trendingScore"),
        "runtime": raw.get("runtime"),
        "subdomain": raw.get("subdomain"),
        "sha": raw.get("sha"),
        "created_at_hf": raw.get("createdAt"),
        "last_modified_hf": raw.get("lastModified"),
        "license": license_value,
        "models": raw.get("models") or [],
        "datasets": raw.get("datasets") or [],
        "source_url": f"https://huggingface.co/spaces/{space_id}",
        "raw_snapshot": raw,
        "observed_at": datetime.now(UTC),
    }


def run_crawl(
    session: Session,
    client: HFClient,
    *,
    limit: int = 500,
    page_size: int = 100,
    refresh: bool = False,
) -> dict:
    """Ingest up to `limit` Spaces, resuming from the checkpoint cursor."""
    checkpoint = session.get(IngestCheckpoint, SOURCE)
    cursor = checkpoint.cursor if checkpoint else None
    total_before = checkpoint.items_seen if checkpoint else 0
    seen = 0
    created = updated = unchanged = refreshed = 0
    failures: list[dict] = list(client.dead_letters)

    while seen < limit:
        page = client.fetch_page(cursor, min(page_size, limit - seen))
        if not page.items:
            break
        for raw in page.items:
            if seen >= limit:
                break
            space_id = raw.get("id")
            if not space_id:
                failures.append({"error": "missing id", "raw": str(raw)[:200]})
                continue
            data = canonicalize(raw)
            row = session.get(HFSpace, space_id)
            if row is None:
                session.add(HFSpace(id=space_id, tenant_id="public", **data))
                created += 1
            elif row.sha == data["sha"]:
                row.observed_at = data["observed_at"]
                row.times_seen = (row.times_seen or 0) + 1
                if refresh and (
                    data["models"] != (row.models or [])
                    or data["datasets"] != (row.datasets or [])
                    or data["raw_snapshot"] != row.raw_snapshot
                ):
                    for key, value in data.items():
                        setattr(row, key, value)
                    refreshed += 1
                else:
                    unchanged += 1
            else:
                history = list(row.snapshot_history or [])
                history.append(
                    {
                        "sha": row.sha,
                        "raw_snapshot": row.raw_snapshot,
                        "observed_at": row.observed_at.isoformat() if row.observed_at else None,
                    }
                )
                for key, value in data.items():
                    setattr(row, key, value)
                row.snapshot_history = history
                row.times_seen = (row.times_seen or 0) + 1
                updated += 1
            seen += 1

        cursor = page.next_cursor
        if checkpoint is None:
            checkpoint = IngestCheckpoint(source=SOURCE)
            session.add(checkpoint)
        checkpoint.cursor = cursor
        checkpoint.updated_at = datetime.now(UTC)
        session.flush()
        if not cursor:
            break

    if checkpoint is None:
        checkpoint = IngestCheckpoint(source=SOURCE, items_seen=seen)
        session.add(checkpoint)
    checkpoint.items_seen = total_before + seen
    checkpoint.updated_at = datetime.now(UTC)
    session.flush()

    return {
        "seen": seen,
        "created": created,
        "updated": updated,
        "unchanged": unchanged,
        "refreshed": refreshed,
        "failures": len(failures),
        "resume_cursor": checkpoint.cursor,
    }