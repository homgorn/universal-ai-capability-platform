"""Seed a small demonstration corpus, build the graph, and generate the wiki."""

from __future__ import annotations

from uaicp.db.base import Base
from uaicp.db.contracts import append_contract
from uaicp.db.models import (
    Capability,
    Execution,
    Interface,
    Operation,
    Provider,
    Resource,
    Tool,
)
from uaicp.db.session import engine, init_db, session_scope
from uaicp.domain.enums import (
    CapabilityStatus,
    EvidenceMark,
    ExecutionStatus,
    InterfaceType,
    ResourceType,
)
from uaicp.graph.rebuild import rebuild_graph
from uaicp.wiki.generate import generate

TENANT = "public"


def seed() -> dict:
    # Idempotent dev seed: rebuild the schema from scratch.
    Base.metadata.drop_all(engine)
    init_db(engine)
    with session_scope(engine) as session:
        provider = Provider(tenant_id=TENANT, name="Hugging Face", kind="HF")
        session.add(provider)
        session.flush()

        resource = Resource(
            tenant_id=TENANT,
            provider_id=provider.id,
            resource_type=ResourceType.SPACE,
            name="background-remover",
            source="hf",
            source_url="https://huggingface.co/spaces/demo/background-remover",
            evidence_mark=EvidenceMark.REPORTED,
            parser_version="1",
            normalized_version="1",
        )
        session.add(resource)
        session.flush()

        iface = Interface(
            tenant_id=TENANT,
            resource_id=resource.id,
            interface_type=InterfaceType.GRADIO,
            source="hf",
            evidence_mark=EvidenceMark.MEASURED,
            schema_snapshot={"api_name": "predict"},
        )
        session.add(iface)
        session.flush()

        operation = Operation(tenant_id=TENANT, name="remove_background")
        session.add(operation)
        session.flush()

        capability = Capability(
            tenant_id=TENANT,
            capability_id="image.background_remove",
            name="Remove image background",
            status=CapabilityStatus.DISCOVERED,
        )
        session.add(capability)
        session.flush()

        tool = Tool(
            tenant_id=TENANT,
            resource_id=resource.id,
            interface_id=iface.id,
            operation_id=operation.id,
            capability_id=capability.id,
            status=CapabilityStatus.DISCOVERED,
            source="hf",
            evidence_mark=EvidenceMark.MEASURED,
        )
        session.add(tool)
        session.flush()

        append_contract(
            session,
            capability,
            inputs={"image": {"semantic_type": "image", "required": True}},
            outputs={"image": {"semantic_type": "image", "required": True}},
        )

        execution = Execution(
            tenant_id=TENANT,
            target_type="TOOL",
            target_id=tool.id,
            status=ExecutionStatus.CREATED,
            idempotency_key="seed-exec-1",
            trace_id="seed-trace-1",
        )
        session.add(execution)
        session.flush()

        triple_count = rebuild_graph(session, TENANT, graph_version=1)

    wiki = generate()
    return {"triples": triple_count, "wiki": wiki}


if __name__ == "__main__":
    result = seed()
    print(f"seeded: {result['triples']} triples; wiki pages={result['wiki']['pages']}")