"""initial schema — all canonical domain + knowledge graph tables

Revision ID: 0001
Revises:
Create Date: 2026-11-25
"""

from __future__ import annotations

from alembic import op

import uaicp.db.models  # noqa: F401  (register models)
from uaicp.db.base import Base

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Foundation MVP: create the full schema from the ORM metadata.
    # Production should replace this with explicit, reviewed DDL.
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())