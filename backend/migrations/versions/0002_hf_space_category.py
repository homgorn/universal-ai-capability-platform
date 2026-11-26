"""add category to hf_space

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("hf_space", sa.Column("category", sa.String(length=64), nullable=True))
    op.create_index("ix_hf_space_category", "hf_space", ["category"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_hf_space_category", table_name="hf_space")
    op.drop_column("hf_space", "category")