"""add_user_id_in_search_logs

Revision ID: 20251030231120398
Revises: 20251030221559188
Create Date: 2025-10-31 07:11:31.755053

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20251030231120398"
down_revision: str | Sequence[str] | None = "20251030221559188"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("search_logs", sa.Column("user_id", sa.UUID(), nullable=False))
    op.create_foreign_key(
        "fk_search_logs_user_id",
        "search_logs",
        "users",
        ["user_id"],
        ["id"],
    )
    op.alter_column("search_logs", "user_id", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_search_logs_user_id", "search_logs", type_="foreignkey")
    op.drop_column("search_logs", "user_id")
