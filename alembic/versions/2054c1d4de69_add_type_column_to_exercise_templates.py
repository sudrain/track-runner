"""add type column to exercise_templates

Revision ID: 2054c1d4de69
Revises: 05a1b2c3d4e5
Create Date: 2026-05-25 17:48:55.424198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2054c1d4de69'
down_revision: Union[str, Sequence[str], None] = '05a1b2c3d4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('exercise_templates') as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=20), nullable=False, server_default='strength'))
        batch_op.create_unique_constraint('uq_exercise_template_name_type', ['name', 'type'])


def downgrade() -> None:
    with op.batch_alter_table('exercise_templates') as batch_op:
        batch_op.drop_constraint('uq_exercise_template_name_type', type_='unique')
        batch_op.drop_column('type')
