"""remove-search-id-unique-constraint-in-search-feedbacks_table

Revision ID: 20251101230647320
Revises: 20251030231120398
Create Date: 2025-11-02 07:07:12.341680

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20251101230647320"
down_revision: str | Sequence[str] | None = "20251030231120398"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("search_feedbacks_search_log_id_key", "search_feedbacks", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint("search_feedbacks_search_log_id_key", "search_feedbacks", ["search_log_id"])
