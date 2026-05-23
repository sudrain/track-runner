"""add revoked_refresh_tokens

Revision ID: 2a1b3c4d5e6f
Revises: 098d6a9e76bb
Create Date: 2026-05-23 13:00:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "2a1b3c4d5e6f"
down_revision: str | None = "098d6a9e76bb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "revoked_refresh_tokens",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "token_jti", sa.String(36), unique=True, nullable=False, index=True
        ),
        sa.Column(
            "revoked_at", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column(
            "expires_at", sa.DateTime(timezone=True), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("revoked_refresh_tokens")
