"""Repository with mandatory tenant scoping (FR-003, SC-003)."""

from __future__ import annotations

from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from uaicp.db.base import Base

T = TypeVar("T", bound=Base)


class TenantRepository:
    """All reads/writes are scoped to a single tenant_id.

    Application-level filtering is the first line of defense; Postgres RLS
    (see migrations) is the second.
    """

    def __init__(self, session: Session, tenant_id: str) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def add(self, obj: T) -> T:
        if getattr(obj, "tenant_id", None) != self.tenant_id:
            raise PermissionError("cross-tenant write is forbidden")
        self.session.add(obj)
        self.session.flush()
        return obj

    def get(self, model: type[T], entity_id: int) -> T | None:
        stmt = select(model).where(
            model.id == entity_id,  # type: ignore[attr-defined]
            model.tenant_id == self.tenant_id,  # type: ignore[attr-defined]
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def list(self, model: type[T]) -> list[T]:
        stmt = select(model).where(model.tenant_id == self.tenant_id)  # type: ignore[attr-defined]
        return list(self.session.execute(stmt).scalars().all())