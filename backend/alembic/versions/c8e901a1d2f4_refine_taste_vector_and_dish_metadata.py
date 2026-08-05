"""refine_taste_vector_and_dish_metadata

Revision ID: c8e901a1d2f4
Revises: e6ad55e22c62
Create Date: 2026-08-02 21:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'c8e901a1d2f4'
down_revision = 'e6ad55e22c62'
branch_labels = None
depends_on = None

def upgrade():
    # Upgrade TasteProfile table: remove adventure_level & portion_preference, add saltiness_preference, oiliness_preference, masala_intensity_preference
    with op.batch_alter_table('taste_profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('saltiness_preference', sa.Float(), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('oiliness_preference', sa.Float(), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('masala_intensity_preference', sa.Float(), nullable=True, server_default='0.5'))

    # Upgrade Dishes table: remove adventure_level & portion_size, add saltiness_level, oiliness_level, masala_intensity
    with op.batch_alter_table('dishes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('saltiness_level', sa.Numeric(precision=4, scale=3), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('oiliness_level', sa.Numeric(precision=4, scale=3), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('masala_intensity', sa.Numeric(precision=4, scale=3), nullable=True, server_default='0.5'))

def downgrade():
    with op.batch_alter_table('taste_profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adventure_level', sa.Float(), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('portion_preference', sa.Float(), nullable=True, server_default='0.5'))
        batch_op.drop_column('masala_intensity_preference')
        batch_op.drop_column('oiliness_preference')
        batch_op.drop_column('saltiness_preference')

    with op.batch_alter_table('dishes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('adventure_level', sa.Numeric(precision=4, scale=3), nullable=True, server_default='0.5'))
        batch_op.add_column(sa.Column('portion_size', sa.Numeric(precision=4, scale=3), nullable=True, server_default='0.5'))
        batch_op.drop_column('masala_intensity')
        batch_op.drop_column('oiliness_level')
        batch_op.drop_column('saltiness_level')
