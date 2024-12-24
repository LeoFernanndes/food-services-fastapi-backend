"""adds recipes ingredient_measurement_units table

Revision ID: 4f5505dfa4e8
Revises: 25010db34341
Create Date: 2024-12-24 17:11:48.777398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f5505dfa4e8'
down_revision: Union[str, None] = '25010db34341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    op.drop_table('ingredient_measurement_units')


def upgrade() -> None:
    op.create_table('ingredient_measurement_units',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False, unique=True),
    sa.PrimaryKeyConstraint('id')
    )
