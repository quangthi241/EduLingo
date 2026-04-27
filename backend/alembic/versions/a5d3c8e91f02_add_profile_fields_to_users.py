"""add profile fields to users

Revision ID: a5d3c8e91f02
Revises: 83048b3ef0fd
Create Date: 2026-04-20 02:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a5d3c8e91f02"
down_revision: str | None = "83048b3ef0fd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("target_cefr", sa.String(length=4), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "goals",
            sa.ARRAY(sa.String(length=64)),
            nullable=False,
            server_default="{}",
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "goals")
    op.drop_column("users", "target_cefr")
