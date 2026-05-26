"""arreglar_pk_profiles_y_crear_sessions

Revision ID: 43c2b6eb92f5
Revises: 8ddb208b5d22
Create Date: 2026-03-11 10:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43c2b6eb92f5'
down_revision: Union[str, None] = '8ddb208b5d22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_primary_key('pk_profiles', 'profiles', ['id'])
    
  
    op.drop_table('sessions')
    
   
    op.create_table('sessions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('distance_meters', sa.Integer(), nullable=False),
    sa.Column('duration_seconds', sa.Integer(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('sessions')
    op.drop_constraint('pk_profiles', 'profiles', type_='primary')