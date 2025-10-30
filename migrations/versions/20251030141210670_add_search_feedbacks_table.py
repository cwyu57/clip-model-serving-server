"""add_search_feedbacks_table

Revision ID: 20251030141210670
Revises: 20251030134405758
Create Date: 2025-10-30 22:12:21.730391

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20251030141210670"
down_revision: str | Sequence[str] | None = "20251030134405758"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "search_feedbacks",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("search_log_id", sa.UUID(), nullable=False),
        sa.Column("is_relevant", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["search_log_id"],
            ["search_logs.id"],
        ),
        sa.UniqueConstraint("search_log_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("search_feedbacks")
