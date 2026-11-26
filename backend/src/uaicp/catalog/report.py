"""Measured inventory report over the canonical HF Space catalog."""

from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import HFSpace


def inventory_report(session: Session) -> dict:
    rows = list(session.execute(select(HFSpace)).scalars().all())
    sdk = Counter(row.sdk or "unknown" for row in rows)
    return {
        "total": len(rows),
        "sdk_distribution": dict(sdk.most_common()),
        "mcp_server": sum(1 for r in rows if "mcp-server" in (r.tags or [])),
        "license_known": sum(1 for r in rows if bool(r.license)),
        "license_unknown": sum(1 for r in rows if not r.license),
        "with_title": sum(1 for r in rows if bool(r.title)),
        "with_models": sum(1 for r in rows if bool(r.models)),
        "with_datasets": sum(1 for r in rows if bool(r.datasets)),
        "unique_sha": len({r.sha for r in rows if r.sha}),
    }