"""add_immutable_unaccent_function

Revision ID: 179f90b23f37
Revises: bae0a10fd169
Create Date: 2025-04-04 10:58:14.982704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '179f90b23f37'
down_revision = 'bae0a10fd169'
branch_labels = None
depends_on = None


def upgrade():
    # No MySQL, não temos funções como unaccent do PostgreSQL
    # Em vez disso, vamos criar índices adequados para busca de texto
    
    # Criar índice FULLTEXT no MySQL para a coluna name
    op.execute('''
    ALTER TABLE product_suggestion 
    ADD FULLTEXT INDEX ft_product_suggestion_name (name);
    ''')
    
    # Também criamos um índice para busca rápida na coluna normalized_name
    op.execute('''
    ALTER TABLE product_suggestion 
    ADD INDEX idx_product_suggestion_normalized_name (normalized_name);
    ''')


def downgrade():
    # Remove os índices criados
    op.execute('ALTER TABLE product_suggestion DROP INDEX ft_product_suggestion_name;')
    op.execute('ALTER TABLE product_suggestion DROP INDEX idx_product_suggestion_normalized_name;')
