"""Contract tests for graph referential integrity (UND-1, edge case)."""

from __future__ import annotations

from uaicp.db.models import KGEntity, KGTriple
from uaicp.domain.enums import EntityType, EvidenceMark
from uaicp.graph.rebuild import prune_orphans


def test_orphan_triple_is_pruned(session):
    node = KGEntity(
        tenant_id="t",
        entity_type=EntityType.TOOL,
        domain_id=1,
        name="tool:1",
        labels=[],
    )
    session.add(node)
    session.flush()

    # object_id points to a non-existent entity (FK disabled in SQLite by default)
    orphan = KGTriple(
        tenant_id="t",
        subject_id=node.id,
        predicate="satisfies",
        object_id=999,
        subject_type=EntityType.TOOL,
        object_type=EntityType.CAPABILITY,
        evidence_mark=EvidenceMark.MEASURED,
        source="test",
        graph_version=1,
    )
    session.add(orphan)
    session.flush()

    removed = prune_orphans(session, "t")
    assert removed == 1
    assert session.query(KGTriple).count() == 0


def test_valid_triple_is_kept(session):
    a = KGEntity(tenant_id="t", entity_type=EntityType.TOOL, domain_id=1, name="tool:1", labels=[])
    b = KGEntity(
        tenant_id="t", entity_type=EntityType.CAPABILITY, domain_id=1, name="cap", labels=[]
    )
    session.add_all([a, b])
    session.flush()
    session.add(
        KGTriple(
            tenant_id="t",
            subject_id=a.id,
            predicate="satisfies",
            object_id=b.id,
            subject_type=EntityType.TOOL,
            object_type=EntityType.CAPABILITY,
            evidence_mark=EvidenceMark.MEASURED,
            source="test",
            graph_version=1,
        )
    )
    session.flush()

    assert prune_orphans(session, "t") == 0
    assert session.query(KGTriple).count() == 1