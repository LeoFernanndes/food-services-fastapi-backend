"""create user table

Revision ID: 5d484d9833ad
Revises: 
Create Date: 2024-07-17 18:25:19.492318

"""
import sqlalchemy as sa

from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5d484d9833ad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('username', sa.TEXT, nullable=False, unique=True),
        sa.Column('email', sa.TEXT(), nullable=False, unique=True),
        sa.Column('password', sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='users_pkey')
    )


def downgrade() -> None:
    op.drop_table('users')
