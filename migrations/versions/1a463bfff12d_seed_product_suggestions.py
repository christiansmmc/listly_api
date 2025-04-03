"""
Seed product suggestions

Revision ID: 1a463bfff12d
Revises: dac3a5dc10c5
Create Date: 2025-04-03 03:20:00.000000

"""
import csv

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic
revision = '1a463bfff12d'
down_revision = 'dac3a5dc10c5'
branch_labels = None
depends_on = None

CSV_FILE = "seed_data/product_suggestions.csv"


def load_seed():
    """Carrega os dados do CSV para uma lista de dicionários."""
    products = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append({"id": int(row["id"]), "name": row["name"]})
    return products


def upgrade():
    """Insere ou atualiza os dados das sugestões de produtos no banco de dados."""
    conn = op.get_bind()
    products = load_seed()

    for product in products:
        conn.execute(
            sa.text(
                """
                INSERT INTO product_suggestion (id, name) VALUES (:id, :name)
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """
            ),
            {"id": product["id"], "name": product["name"]}
        )


def downgrade():
    """Remove os registros inseridos na operação de upgrade."""
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM product_suggestion WHERE id BETWEEN 1 AND 100;")) 