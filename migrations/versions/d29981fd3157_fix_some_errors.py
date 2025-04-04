"""Fix some errors

Revision ID: d29981fd3157
Revises: 179f90b23f37
Create Date: 2025-04-04 11:25:26.947327

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd29981fd3157'
down_revision = '179f90b23f37'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index('ft_product_suggestion_name', table_name='product_suggestion')
    op.drop_index('idx_product_suggestion_normalized_name', table_name='product_suggestion')

    with op.batch_alter_table('product_suggestion') as batch_op:
        batch_op.drop_constraint('name', type_='unique')
        batch_op.alter_column(
            'name',
            type_=sa.String(length=100),
            existing_type=sa.String(length=255),
            nullable=False
        )


def downgrade():
    # Recria o FULLTEXT index (caso você realmente precise dele)
    # Mas lembre que o Alembic 'create_index' não tem suporte direto para FULLTEXT;
    # se precisar, você pode voltar a usar 'op.execute("ALTER TABLE ... ADD FULLTEXT INDEX ...")'
    op.create_index('ft_product_suggestion_name', 'product_suggestion', ['name'])
    op.create_index('idx_product_suggestion_normalized_name', 'product_suggestion', ['normalized_name'])

    with op.batch_alter_table('product_suggestion') as batch_op:
        batch_op.create_unique_constraint('name', ['name'])
        batch_op.alter_column(
            'name',
            type_=sa.String(length=255),
            existing_type=sa.String(length=100),
            nullable=False
        )
