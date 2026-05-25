"""seed exercise templates

Revision ID: 05a1b2c3d4e5
Revises: 04f938201019
Create Date: 2026-05-25 17:39:00.000000

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import String
from sqlalchemy.sql import column, table

revision: str = "05a1b2c3d4e5"
down_revision: Union[str, Sequence[str], None] = "04f938201019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    exercise_templates = table(
        "exercise_templates",
        column("name", String),
    )
    op.bulk_insert(
        exercise_templates,
        [
            {"name": "Жим штанги лёжа"},
            {"name": "Приседания со штангой"},
            {"name": "Становая тяга"},
            {"name": "Жим гантелей сидя"},
            {"name": "Тяга штанги в наклоне"},
            {"name": "Подтягивания"},
            {"name": "Отжимания на брусьях"},
            {"name": "Сгибание рук со штангой"},
            {"name": "Французский жим"},
            {"name": "Выпады с гантелями"},
            {"name": "Жим ногами"},
            {"name": "Тяга верхнего блока"},
            {"name": "Разводка гантелей лёжа"},
            {"name": "Скручивания"},
            {"name": "Планка"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM exercise_templates")
