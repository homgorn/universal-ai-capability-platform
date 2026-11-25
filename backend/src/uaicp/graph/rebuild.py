"""Deterministic graph rebuild from the canonical store (derived projection)."""

from __future__ import annotations

from sqlalchemy import and_, delete, or_, select
from sqlalchemy.orm import Session

from uaicp.db.models import KGEntity, KGTriple
from uaicp.graph.extract import GraphExtractor


def prune_orphans(session: Session, tenant_id: str) -> int:
    """Remove triples whose subject/object entity is missing (referential integrity).

    Handles the edge case "a triple referencing a deleted/unknown entity" without
    orphaning the graph. Returns the number of removed triples.
    """
    entity_ids = select(KGEntity.id).where(KGEntity.tenant_id == tenant_id)
    orphan_condition = or_(
        KGTriple.subject_id.notin_(entity_ids),
        and_(
            KGTriple.object_id.isnot(None),
            KGTriple.object_id.notin_(entity_ids),
        ),
    )
    orphan_ids = list(
        session.execute(
            select(KGTriple.id).where(
                KGTriple.tenant_id == tenant_id,
                orphan_condition,
            )
        ).scalars().all()
    )
    if not orphan_ids:
        return 0
    session.execute(delete(KGTriple).where(KGTriple.id.in_(orphan_ids)))
    return len(orphan_ids)


def rebuild_graph(session: Session, tenant_id: str, graph_version: int = 1) -> int:
    """Drop this tenant's graph projection and rebuild it deterministically.

    Only derived tables (kg_triple, kg_entity) are touched; canonical domain
    rows and immutable contracts are never modified. Returns the number of
    triples remaining after orphan pruning.
    """
    session.execute(delete(KGTriple).where(KGTriple.tenant_id == tenant_id))
    session.execute(delete(KGEntity).where(KGEntity.tenant_id == tenant_id))
    session.flush()
    GraphExtractor(session, tenant_id, graph_version).extract()
    session.flush()
    prune_orphans(session, tenant_id)
    session.flush()
    remaining = session.execute(
        select(KGTriple.id).where(KGTriple.tenant_id == tenant_id)
    ).all()
    return len(remaining)