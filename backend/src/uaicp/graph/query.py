"""Triple pattern queries (contract: graph-query.md)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import KGTriple


def query_triples(
    session: Session,
    tenant_id: str,
    *,
    subject_id: int | None = None,
    predicate: str | None = None,
    object_id: int | None = None,
    object_literal: str | None = None,
) -> list[KGTriple]:
    """Return triples matching the pattern, always tenant-filtered.

    Pattern forms: s??, ? ?o, s p?, ? p o, s?o (see contracts/graph-query.md).
    Unknown predicate returns an empty list, not an error.
    """
    stmt = select(KGTriple).where(KGTriple.tenant_id == tenant_id)
    if subject_id is not None:
        stmt = stmt.where(KGTriple.subject_id == subject_id)
    if predicate is not None:
        stmt = stmt.where(KGTriple.predicate == predicate)
    if object_id is not None:
        stmt = stmt.where(KGTriple.object_id == object_id)
    if object_literal is not None:
        stmt = stmt.where(KGTriple.object_literal == object_literal)
    stmt = stmt.order_by(KGTriple.id)
    return list(session.execute(stmt).scalars().all())