"""Make UserProfile.username unique.

Revision ID: 0b9f3f5d6c2a
Revises: 
Create Date: 2026-03-06
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "0b9f3f5d6c2a"
down_revision = "181361ce1714"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # If duplicates already exist, make them unique by appending suffix.
    op.execute(
        """
        WITH dups AS (
            SELECT
                id,
                username,
                row_number() OVER (PARTITION BY username ORDER BY id) AS rn
            FROM "UserProfile"
        )
        UPDATE "UserProfile" u
        SET username = u.username || '__dup_' || u.id
        FROM dups
        WHERE u.id = dups.id AND dups.rn > 1
        """
    )
    op.create_unique_constraint(
        "uq_userprofile_username",
        "UserProfile",
        ["username"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_userprofile_username",
        "UserProfile",
        type_="unique",
    )
