"""Add due/done/favorite metadata to tasks.

Revision ID: 3a51c85e4e33
Revises: 0b9f3f5d6c2a
Create Date: 2026-03-10
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a51c85e4e33"
down_revision = "0b9f3f5d6c2a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "Tasks",
        sa.Column("due", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "Tasks",
        sa.Column("done", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "Tasks",
        sa.Column("favorite", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )


def downgrade() -> None:
    op.drop_column("Tasks", "favorite")
    op.drop_column("Tasks", "done")
    op.drop_column("Tasks", "due")
