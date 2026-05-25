"""drop old unique(name) constraint

Revision ID: d866946d2097
Revises: 2054c1d4de69
Create Date: 2026-05-25 17:50:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'd866946d2097'
down_revision: Union[str, Sequence[str], None] = '2054c1d4de69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute(
            "ALTER TABLE exercise_templates "
            "DROP CONSTRAINT IF EXISTS exercise_templates_name_key"
        )
    else:
        op.execute("""
            CREATE TABLE exercise_templates_new (
                id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20) NOT NULL DEFAULT 'strength',
                PRIMARY KEY (id),
                CONSTRAINT uq_exercise_template_name_type UNIQUE (name, type)
            )
        """)
        op.execute(
            "INSERT INTO exercise_templates_new (id, name, type) "
            "SELECT id, name, type FROM exercise_templates"
        )
        op.execute("DROP TABLE exercise_templates")
        op.execute("ALTER TABLE exercise_templates_new RENAME TO exercise_templates")


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        op.execute(
            "ALTER TABLE exercise_templates "
            "ADD CONSTRAINT exercise_templates_name_key UNIQUE (name)"
        )
    else:
        op.execute("""
            CREATE TABLE exercise_templates_old (
                id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(20) NOT NULL DEFAULT 'strength',
                PRIMARY KEY (id),
                UNIQUE (name),
                CONSTRAINT uq_exercise_template_name_type UNIQUE (name, type)
            )
        """)
        op.execute(
            "INSERT INTO exercise_templates_old (id, name, type) "
            "SELECT id, name, type FROM exercise_templates"
        )
        op.execute("DROP TABLE exercise_templates")
        op.execute("ALTER TABLE exercise_templates_old RENAME TO exercise_templates")
