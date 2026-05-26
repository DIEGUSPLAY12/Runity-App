"""add image_url to challenges

Revision ID: 4bb1c5b82ae1
Revises: b35742326baf
Create Date: 2026-04-08 10:04:44.943206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bb1c5b82ae1'
down_revision: Union[str, Sequence[str], None] = 'b35742326baf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Añadimos SOLO la columna de la imagen
    op.add_column('challenges', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Borramos SOLO la columna de la imagen en caso de revertir
    op.drop_column('challenges', 'image_url')