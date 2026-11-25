"""Contract tests for graph triple queries (contracts/graph-query.md, SC-005)."""

from __future__ import annotations

from uaicp.db.models import (
    Capability,
    Interface,
    Operation,
    Provider,
    Resource,
    Tool,
)
from uaicp.domain.enums import (
    CapabilityStatus,
    EvidenceMark,
    InterfaceType,
    ResourceType,
)
from uaicp.graph.query import query_triples
from uaicp.graph.rebuild import rebuild_graph


def _seed(session) -> None:
    p = Provider(tenant_id="t", name="HF", kind="HF")
    session.add(p)
    session.flush()
    r = Resource(
        tenant_id="t",
        provider_id=p.id,
        resource_type=ResourceType.SPACE,
        name="bg",
        source="hf",
        evidence_mark=EvidenceMark.MEASURED,
    )
    session.add(r)
    session.flush()
    i = Interface(
        tenant_id="t",
        resource_id=r.id,
        interface_type=InterfaceType.GRADIO,
        source="hf",
        evidence_mark=EvidenceMark.MEASURED,
    )
    session.add(i)
    session.flush()
    o = Operation(tenant_id="t", name="remove_background")
    session.add(o)
    session.flush()
    c = Capability(
        tenant_id="t",
        capability_id="image.background_remove",
        name="bg",
        status=CapabilityStatus.DISCOVERED,
    )
    session.add(c)
    session.flush()
    tool = Tool(
        tenant_id="t",
        resource_id=r.id,
        interface_id=i.id,
        operation_id=o.id,
        capability_id=c.id,
        status=CapabilityStatus.DISCOVERED,
        source="hf",
        evidence_mark=EvidenceMark.MEASURED,
    )
    session.add(tool)
    session.flush()


def test_rebuild_creates_expected_triples(session):
    _seed(session)
    count = rebuild_graph(session, "t", graph_version=1)
    assert count >= 4  # owns, exposes, implements, satisfies

    triples = query_triples(session, "t", predicate="satisfies")
    assert len(triples) == 1
    assert triples[0].object_type is not None


def test_pattern_queries(session):
    _seed(session)
    rebuild_graph(session, "t")

    owns = query_triples(session, "t", predicate="owns")
    assert len(owns) == 1

    # unknown predicate -> empty, not error
    assert query_triples(session, "t", predicate="unknown") == []


def test_tenant_filtering_in_graph(session):
    _seed(session)
    rebuild_graph(session, "t")
    # tenant B sees nothing
    assert query_triples(session, "B") == []