"""Idempotency contract tests (US1, SC-001)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.models import Execution
from uaicp.execution.gateway import create_execution


def _create(session: Session, tenant: str, key: str) -> Execution:
    return create_execution(
        session, tenant, target_type="TOOL", target_id=1,
        idempotency_key=key, trace_id=f"trace-{key}",
    )


def test_duplicate_key_returns_same_execution(session):
    first = _create(session, "A", "key-1")
    second = _create(session, "A", "key-1")
    assert first.id == second.id
    assert session.execute(select(Execution)).scalars().all().__len__() == 1


def test_same_key_different_tenant_isolated(session):
    a = _create(session, "A", "key-1")
    b = _create(session, "B", "key-1")
    assert a.id != b.id