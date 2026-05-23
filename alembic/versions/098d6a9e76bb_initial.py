"""initial

Revision ID: 098d6a9e76bb
Revises:
Create Date: 2026-05-23 12:29:38.333786

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "098d6a9e76bb"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "cardio_workouts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text, default=""),
    )

    op.create_table(
        "cardio_intervals",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "workout_id",
            sa.Integer,
            sa.ForeignKey("cardio_workouts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("duration_minutes", sa.Float, nullable=False),
        sa.Column("distance_km", sa.Float, nullable=False),
        sa.Column("tempo_min_per_km", sa.Float, nullable=True),
        sa.Column("avg_heart_rate", sa.Integer, nullable=True),
    )

    op.create_table(
        "strength_workouts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text, default=""),
    )

    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "workout_id",
            sa.Integer,
            sa.ForeignKey("strength_workouts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("name", sa.String(100), nullable=False),
    )

    op.create_table(
        "sets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "exercise_id",
            sa.Integer,
            sa.ForeignKey("exercises.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("weight_kg", sa.Float, nullable=False),
        sa.Column("repetitions", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("sets")
    op.drop_table("exercises")
    op.drop_table("strength_workouts")
    op.drop_table("cardio_intervals")
    op.drop_table("cardio_workouts")
    op.drop_table("users")
