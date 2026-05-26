"""setup presence rls and realtime

Revision ID: d1996f4093eb
Revises: 73b614580132
Create Date: 2026-04-14 10:44:50.232641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1996f4093eb'
down_revision: Union[str, Sequence[str], None] = '73b614580132'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Activar Seguridad a Nivel de Fila (RLS) en la tabla presence
    op.execute("ALTER TABLE presence ENABLE ROW LEVEL SECURITY;")
    
    # 2. Crear la política de lectura (SELECT)
    # Usamos auth.uid() que es la forma en la que Supabase identifica al usuario conectado
    op.execute("""
        CREATE POLICY "ver_presencia_amigos" ON presence
        FOR SELECT
        USING (
            -- El usuario puede ver su propia presencia
            user_id = auth.uid() 
            OR 
            -- O la presencia de la gente a la que sigue
            user_id IN (
                SELECT followed_id FROM follows WHERE follower_id = auth.uid()
            )
        );
    """)

    # 3. Añadir la tabla a la publicación de Supabase Realtime
    op.execute("ALTER PUBLICATION supabase_realtime ADD TABLE presence;")


def downgrade() -> None:
    # Revertir los cambios en orden inverso en caso de rollback
    op.execute("ALTER PUBLICATION supabase_realtime DROP TABLE presence;")
    op.execute("DROP POLICY IF EXISTS \"ver_presencia_amigos\" ON presence;")
    op.execute("ALTER TABLE presence DISABLE ROW LEVEL SECURITY;")
