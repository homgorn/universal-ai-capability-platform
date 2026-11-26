"""Derived knowledge graph for the HF Space catalog (entities + triples)."""

from __future__ import annotations

import hashlib

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from uaicp.catalog.taxonomy import categorize
from uaicp.db.models import HFSpace, KGEntity, KGTriple
from uaicp.domain.enums import EntityType, EvidenceMark

TENANT = "public"
CATALOG_TYPES = {
    EntityType.SPACE_APP,
    EntityType.TAG,
    EntityType.SDK,
    EntityType.LICENSE,
    EntityType.MODEL,
    EntityType.DATASET,
    EntityType.AUTHOR,
    EntityType.CATEGORY,
}


def _node_id(kind: str, value: str) -> int:
    return int(hashlib.sha256(f"{kind}:{value}".encode()).hexdigest()[:12], 16)


def build_catalog_graph(session: Session) -> dict:
    """Rebuild catalog-derived entities/triples. Canonical domain rows are untouched."""
    session.execute(
        delete(KGTriple).where(
            KGTriple.tenant_id == TENANT,
            KGTriple.subject_type.in_(list(CATALOG_TYPES)),
        )
    )
    session.execute(
        delete(KGEntity).where(
            KGEntity.tenant_id == TENANT,
            KGEntity.entity_type.in_(list(CATALOG_TYPES)),
        )
    )
    session.flush()

    nodes: dict[tuple[EntityType, int], int] = {}

    def node(kind: EntityType, value: str, name: str) -> int:
        domain_id = _node_id(kind.value, value)
        key = (kind, domain_id)
        if key in nodes:
            return nodes[key]
        row = KGEntity(
            tenant_id=TENANT,
            entity_type=kind,
            domain_id=domain_id,
            name=name[:255],
            labels=["catalog"],
        )
        session.add(row)
        session.flush()
        nodes[key] = row.id
        return row.id

    triples = 0

    def edge(
        subject: int,
        subject_type: EntityType,
        predicate: str,
        obj: int,
        object_type: EntityType,
    ) -> None:
        nonlocal triples
        session.add(
            KGTriple(
                tenant_id=TENANT,
                subject_id=subject,
                predicate=predicate,
                object_id=obj,
                subject_type=subject_type,
                object_type=object_type,
                evidence_mark=EvidenceMark.MEASURED,
                source="hf-api",
                source_url="https://huggingface.co/api/spaces",
                graph_version=1,
            )
        )
        triples += 1

    rows = list(session.execute(select(HFSpace)).scalars().all())
    for row in rows:
        space = node(EntityType.SPACE_APP, row.id, row.title or row.id)
        category = node(EntityType.CATEGORY, row.category or "other", row.category or "other")
        edge(space, EntityType.SPACE_APP, "in_category", category, EntityType.CATEGORY)

        sdk = node(EntityType.SDK, row.sdk or "unknown", row.sdk or "unknown")
        edge(space, EntityType.SPACE_APP, "uses_sdk", sdk, EntityType.SDK)

        license_value = row.license or "unknown"
        lic = node(EntityType.LICENSE, license_value, license_value)
        edge(space, EntityType.SPACE_APP, "has_license", lic, EntityType.LICENSE)

        if row.author:
            author = node(EntityType.AUTHOR, row.author, row.author)
            edge(space, EntityType.SPACE_APP, "authored_by", author, EntityType.AUTHOR)

        for tag in row.tags or []:
            if str(tag).startswith("region:"):
                continue
            tag_node = node(EntityType.TAG, str(tag), str(tag))
            edge(space, EntityType.SPACE_APP, "tagged", tag_node, EntityType.TAG)

        if categorize(row.tags) != (row.category or "other"):
            # keep graph consistent even before a DB backfill
            cat2 = node(EntityType.CATEGORY, categorize(row.tags), categorize(row.tags))
            edge(space, EntityType.SPACE_APP, "in_category", cat2, EntityType.CATEGORY)

        for model in (row.models or [])[:5]:
            m = node(EntityType.MODEL, str(model), str(model))
            edge(space, EntityType.SPACE_APP, "linked_model", m, EntityType.MODEL)
        for dataset in (row.datasets or [])[:5]:
            d = node(EntityType.DATASET, str(dataset), str(dataset))
            edge(space, EntityType.SPACE_APP, "linked_dataset", d, EntityType.DATASET)

    session.flush()
    return {
        "spaces": len(rows),
        "entities": session.query(KGEntity).filter(KGEntity.tenant_id == TENANT).count(),
        "triples": triples,
    }