"""Read-only knowledge API (SPECS.md §13, subset for the Knowledge Foundation)."""

from __future__ import annotations

from collections.abc import Iterator

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import Capability, Tool
from uaicp.db.session import SessionLocal
from uaicp.graph.query import query_triples

router = APIRouter(prefix="/v1")


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_tenant(x_tenant_id: str = Header(default="public", alias="X-Tenant-ID")) -> str:
    return x_tenant_id


@router.get("/capabilities")
def list_capabilities(
    tenant: str = Depends(get_tenant),
    session: Session = Depends(get_session),
):
    rows = session.execute(
        select(Capability).where(Capability.tenant_id == tenant).order_by(Capability.id)
    ).scalars().all()
    return {
        "request_id": "local",
        "trace_id": "local",
        "data": [
            {
                "id": c.id,
                "capability_id": c.capability_id,
                "name": c.name,
                "status": c.status.value,
            }
            for c in rows
        ],
    }


@router.get("/capabilities/{capability_id}")
def get_capability(
    capability_id: int,
    tenant: str = Depends(get_tenant),
    session: Session = Depends(get_session),
):
    row = session.execute(
        select(Capability).where(
            Capability.id == capability_id, Capability.tenant_id == tenant
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="capability not found")
    return {
        "request_id": "local",
        "trace_id": "local",
        "data": {
            "id": row.id,
            "capability_id": row.capability_id,
            "name": row.name,
            "status": row.status.value,
        },
    }


@router.get("/tools/{tool_id}/contract")
def tool_contract(
    tool_id: int,
    tenant: str = Depends(get_tenant),
    session: Session = Depends(get_session),
):
    tool = session.execute(
        select(Tool).where(Tool.id == tool_id, Tool.tenant_id == tenant)
    ).scalar_one_or_none()
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    return {
        "request_id": "local",
        "trace_id": "local",
        "data": {"tool_id": tool.id, "capability_id": tool.capability_id},
    }


@router.get("/triples")
def triples(
    tenant: str = Depends(get_tenant),
    subject_id: int | None = Query(default=None),
    predicate: str | None = Query(default=None),
    object_id: int | None = Query(default=None),
    session: Session = Depends(get_session),
):
    rows = query_triples(
        session,
        tenant,
        subject_id=subject_id,
        predicate=predicate,
        object_id=object_id,
    )
    return {
        "request_id": "local",
        "trace_id": "local",
        "data": {
            "triples": [
                {
                    "subject_id": t.subject_id,
                    "predicate": t.predicate,
                    "object_id": t.object_id,
                    "object_literal": t.object_literal,
                    "evidence_mark": t.evidence_mark.value,
                    "graph_version": t.graph_version,
                }
                for t in rows
            ]
        },
    }