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
    
    # Criando índice GIN para busca de texto na tabela product_suggestion
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_product_suggestion_name_gin
    ON product_suggestion
    USING gin(to_tsvector('portuguese', unaccent(name)))
    """)


def downgrade():
    # Removendo o índice GIN
    op.execute("DROP INDEX IF EXISTS idx_product_suggestion_name_gin") 