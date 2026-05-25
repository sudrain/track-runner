"""seed cardio exercise templates

Revision ID: e5f4e3d2c1b0
Revises: d866946d2097
Create Date: 2026-05-25 17:51:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import String
from sqlalchemy.sql import column, table

revision: str = "e5f4e3d2c1b0"
down_revision: Union[str, Sequence[str], None] = "d866946d2097"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    exercise_templates = table(
        "exercise_templates",
        column("name", String),
        column("type", String),
    )
    op.bulk_insert(
        exercise_templates,
        [
            {"name": "Бег на улице", "type": "cardio"},
            {"name": "Бег на беговой дорожке", "type": "cardio"},
            {"name": "Ходьба на улице в среднем темпе", "type": "cardio"},
            {"name": "Быстрая ходьба", "type": "cardio"},
            {"name": "Скандинавская ходьба", "type": "cardio"},
            {"name": "Спортивная ходьба", "type": "cardio"},
            {"name": "Интервальный бег", "type": "cardio"},
            {"name": "Лёгкая пробежка", "type": "cardio"},
            {"name": "Бег в горку", "type": "cardio"},
            {"name": "Бег по лестнице", "type": "cardio"},
            {"name": "Велотренировка (шоссе)", "type": "cardio"},
            {"name": "Велотренировка (велотренажёр)", "type": "cardio"},
            {"name": "Плавание", "type": "cardio"},
            {"name": "Эллиптический тренажёр", "type": "cardio"},
            {"name": "Гребной тренажёр", "type": "cardio"},
            {"name": "Степпер", "type": "cardio"},
            {"name": "HIIT кардио", "type": "cardio"},
            {"name": "Разминка / Заминка", "type": "cardio"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM exercise_templates WHERE type = 'cardio'")
