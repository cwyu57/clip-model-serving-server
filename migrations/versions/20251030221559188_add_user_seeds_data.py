"""add_user_seeds_data

Revision ID: 20251030221559188
Revises: 20251030221112207
Create Date: 2025-10-31 06:16:14.075041

"""

from collections.abc import Sequence

import bcrypt
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20251030221559188"
down_revision: str | Sequence[str] | None = "20251030221112207"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert 5 test users with hashed password "password123"
    hashed_password = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode("utf-8")

    users_table = sa.table(
        "users",
        sa.column("username", sa.String),
        sa.column("email", sa.String),
        sa.column("hashed_password", sa.String),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "username": "user-1",
                "hashed_password": hashed_password,
            },
            {
                "username": "user-2",
                "hashed_password": hashed_password,
            },
            {
                "username": "user-3",
                "hashed_password": hashed_password,
            },
            {
                "username": "user-4",
                "hashed_password": hashed_password,
            },
            {
                "username": "user-5",
                "hashed_password": hashed_password,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the test users
    op.execute(
        """
        DELETE FROM users
        WHERE username IN ('user-1', 'user-2', 'user-3', 'user-4', 'user-5')
        """
    )
