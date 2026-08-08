"""add notification title and type

Revision ID: 5a73fd129e4a
Revises:
Create Date: 2026-08-02 23:01:46.641082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a73fd129e4a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""

    op.add_column(
        "notifications",
        sa.Column(
            "title",
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        "notifications",
        sa.Column(
            "notification_type",
            sa.String(length=50),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade database schema."""

    op.drop_column(
        "notifications",
        "notification_type"
    )

    op.drop_column(
        "notifications",
        "title"
    )