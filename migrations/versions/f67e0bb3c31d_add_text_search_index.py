"""add text search index

Revision ID: f67e0bb3c31d
Revises: 041949490566
Create Date: 2025-04-03 00:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f67e0bb3c31d'
down_revision = '041949490566'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionando extensão unaccent se não existir
    op.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
    
    # Usando btree para indexar a coluna normalized_name (que já existe e não tem acentos)
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_product_suggestion_normalized_name_btree
    ON product_suggestion 
    USING btree(normalized_name text_pattern_ops)
    """)
    
    # Torna a função unaccent IMMUTABLE (necessário para uso em índices)
    op.execute("""
    CREATE OR REPLACE FUNCTION public.immutable_unaccent(text)
    RETURNS text
    LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT
    AS $function$
    SELECT unaccent($1)
    $function$;
    """)
    
    # Criando índice GIN para busca de texto com nossa função IMMUTABLE
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_product_suggestion_name_gin
    ON product_suggestion
    USING gin(to_tsvector('portuguese', immutable_unaccent(name)))
    """)


def downgrade():
    # Removendo os índices
    op.execute("DROP INDEX IF EXISTS idx_product_suggestion_name_gin")
    op.execute("DROP INDEX IF EXISTS idx_product_suggestion_normalized_name_btree")
    op.execute("DROP FUNCTION IF EXISTS public.immutable_unaccent(text)") 