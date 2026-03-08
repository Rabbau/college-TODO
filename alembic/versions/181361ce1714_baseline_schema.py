"""Baseline schema for existing models.

This revision exists because the database already has an Alembic version
stamped as 181361ce1714. The original migration file was missing from the repo.

Revision ID: 181361ce1714
Revises:
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "181361ce1714"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "UserProfile",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
    )

    op.create_table(
        "Categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
    )

    op.create_table(
        "Tasks",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("pomodoro", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("UserProfile.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("Tasks")
    op.drop_table("Categories")
    op.drop_table("UserProfile")
