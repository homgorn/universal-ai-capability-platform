"""Triple extraction: derive (subject, predicate, object) edges from domain rows."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import (
    Capability,
    ContractVersion,
    Execution,
    Interface,
    KGEntity,
    KGTriple,
    Operation,
    Provider,
    Resource,
    Tool,
)
from uaicp.domain.enums import EntityType, EvidenceMark


def _now() -> datetime:
    return datetime.now(UTC)


class GraphExtractor:
    """Builds graph nodes and edges for one tenant from the canonical store."""

    def __init__(self, session: Session, tenant_id: str, graph_version: int = 1) -> None:
        self.session = session
        self.tenant_id = tenant_id
        self.graph_version = graph_version
        self._node_cache: dict[tuple[str, int], KGEntity] = {}

    def node(self, entity_type: EntityType, domain_id: int, name: str) -> KGEntity:
        key = (entity_type.value, domain_id)
        if key in self._node_cache:
            return self._node_cache[key]
        stmt = select(KGEntity).where(
            KGEntity.tenant_id == self.tenant_id,
            KGEntity.entity_type == entity_type,
            KGEntity.domain_id == domain_id,
        )
        node = self.session.execute(stmt).scalar_one_or_none()
        if node is None:
            node = KGEntity(
                tenant_id=self.tenant_id,
                entity_type=entity_type,
                domain_id=domain_id,
                name=name,
                labels=[],
            )
            self.session.add(node)
            self.session.flush()
        self._node_cache[key] = node
        return node

    def edge(
        self,
        subject: KGEntity,
        predicate: str,
        obj: KGEntity | None = None,
        literal: str | None = None,
        *,
        mark: EvidenceMark = EvidenceMark.INFERRED,
        source: str = "platform",
        source_url: str | None = None,
        observed_at: datetime | None = None,
    ) -> KGTriple:
        triple = KGTriple(
            tenant_id=self.tenant_id,
            subject_id=subject.id,
            predicate=predicate,
            object_id=obj.id if obj else None,
            object_literal=literal,
            subject_type=subject.entity_type,
            object_type=obj.entity_type if obj else None,
            evidence_mark=mark,
            source=source,
            source_url=source_url,
            observed_at=observed_at or _now(),
            graph_version=self.graph_version,
        )
        self.session.add(triple)
        return triple

    def extract(self) -> list[KGTriple]:
        triples: list[KGTriple] = []
        t = self.tenant_id

        providers = self.session.execute(
            select(Provider).where(Provider.tenant_id == t)
        ).scalars().all()
        for p in providers:
            self.node(EntityType.PROVIDER, p.id, p.name)

        resources = self.session.execute(
            select(Resource).where(Resource.tenant_id == t)
        ).scalars().all()
        for r in resources:
            rnode = self.node(EntityType.RESOURCE, r.id, r.name)
            provider = self.session.get(Provider, r.provider_id)
            if provider and provider.tenant_id == t:
                pnode = self.node(EntityType.PROVIDER, provider.id, provider.name)
                triples.append(
                    self.edge(pnode, "owns", rnode, mark=r.evidence_mark, source=r.source)
                )

        interfaces = self.session.execute(
            select(Interface).where(Interface.tenant_id == t)
        ).scalars().all()
        for i in interfaces:
            inode = self.node(EntityType.INTERFACE, i.id, i.interface_type.value)
            resource = self.session.get(Resource, i.resource_id)
            if resource and resource.tenant_id == t:
                rnode = self.node(EntityType.RESOURCE, resource.id, resource.name)
                triples.append(
                    self.edge(rnode, "exposes", inode, mark=i.evidence_mark, source=i.source)
                )

        operations = self.session.execute(
            select(Operation).where(Operation.tenant_id == t)
        ).scalars().all()
        for o in operations:
            self.node(EntityType.OPERATION, o.id, o.name)

        capabilities = self.session.execute(
            select(Capability).where(Capability.tenant_id == t)
        ).scalars().all()
        for c in capabilities:
            self.node(EntityType.CAPABILITY, c.id, c.capability_id)

        tools = self.session.execute(select(Tool).where(Tool.tenant_id == t)).scalars().all()
        for tool in tools:
            tnode = self.node(EntityType.TOOL, tool.id, f"tool:{tool.id}")
            op = self.session.get(Operation, tool.operation_id)
            if op and op.tenant_id == t:
                onode = self.node(EntityType.OPERATION, op.id, op.name)
                triples.append(
                    self.edge(
                        tnode,
                        "implements",
                        onode,
                        mark=tool.evidence_mark,
                        source=tool.source,
                    )
                )
            if tool.capability_id:
                cap = self.session.get(Capability, tool.capability_id)
                if cap and cap.tenant_id == t:
                    cnode = self.node(EntityType.CAPABILITY, cap.id, cap.capability_id)
                    triples.append(
                        self.edge(
                            tnode,
                            "satisfies",
                            cnode,
                            mark=tool.evidence_mark,
                            source=tool.source,
                        )
                    )

        # capability has contract (latest version)
        for c in capabilities:
            latest = self.session.execute(
                select(ContractVersion)
                .where(ContractVersion.capability_id == c.id)
                .order_by(ContractVersion.version.desc())
            ).scalars().first()
            if latest:
                cnode = self.node(EntityType.CAPABILITY, c.id, c.capability_id)
                triples.append(
                    self.edge(
                        cnode,
                        "has_contract",
                        literal=f"v{latest.version}:{latest.fingerprint}",
                        mark=EvidenceMark.MEASURED,
                        source="platform",
                    )
                )

        executions = self.session.execute(
            select(Execution).where(Execution.tenant_id == t)
        ).scalars().all()
        for e in executions:
            if e.target_type == "TOOL":
                exec_tool = self.session.get(Tool, e.target_id)
                if exec_tool and exec_tool.tenant_id == t:
                    enode = self.node(EntityType.EXECUTION, e.id, f"execution:{e.id}")
                    tnode = self.node(EntityType.TOOL, exec_tool.id, f"tool:{exec_tool.id}")
                    triples.append(
                        self.edge(
                            enode,
                            "targets",
                            tnode,
                            mark=EvidenceMark.MEASURED,
                            source="platform",
                        )
                    )

        self.session.flush()
        return triples