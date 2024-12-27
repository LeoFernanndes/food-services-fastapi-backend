"""adds recipes related tables

Revision ID: 3e2093d41384
Revises: 4f5505dfa4e8
Create Date: 2024-12-24 20:30:05.162830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e2093d41384'
down_revision: Union[str, None] = '4f5505dfa4e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    op.drop_table('recipe_ingredients')
    op.drop_table('ingredients')
    op.drop_table('recipes')
    op.drop_table('recipe_categories')


def upgrade() -> None:
    op.create_table('recipe_categories',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='recipe_categories_pkey')
    )

    op.create_table('recipes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.Column('user_profile_id', sa.INTEGER(), nullable=False),
    sa.Column('preparation_time_minutes', sa.INTEGER(), nullable=False),
    sa.Column('preparation_steps', sa.VARCHAR(), nullable=False),
    sa.Column('main_image', sa.VARCHAR(), nullable=False),
    sa.Column('portions_quantity', sa.INTEGER(), nullable=False),
    sa.Column('category_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], name='recipes_user_profile_id_fkey'),
    sa.ForeignKeyConstraint(['category_id'], ['recipe_categories.id'], name='recipes_recipe_category_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='recipes_pkey')
    )

    op.create_table('ingredients',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False, unique=True),
    sa.PrimaryKeyConstraint('id', name='ingredients_pkey')
    )

    op.create_table('recipe_ingredients',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('quantity', sa.INTEGER(), nullable=False),
    sa.Column('ingredient_id', sa.INTEGER(), nullable=False),
    sa.Column('ingredient_measurement_unit_id', sa.INTEGER(), nullable=False),
    sa.Column('recipe_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['ingredient_measurement_unit_id'], ['ingredient_measurement_units.id'], name='recipe_ingredients_ingredient_measurement_unit_id_fkey'),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], name='recipe_ingredients_recipe_id_fkey'),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], name='recipe_ingredients_ingredient_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='recipe_ingredients_pkey')
    )
