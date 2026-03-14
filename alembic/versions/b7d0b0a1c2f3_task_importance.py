"""Add importance to tasks.

Revision ID: b7d0b0a1c2f3
Revises: 3a51c85e4e33
Create Date: 2026-03-13
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b7d0b0a1c2f3"
down_revision = "3a51c85e4e33"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Tasks",
        # made by kirill
        sa.Column(
            "importance",
            sa.String(50),
            nullable=False,
            server_default="нейтрально",
        ),
        # made by kirill
    )


def downgrade() -> None:
    op.drop_column("Tasks", "importance")
