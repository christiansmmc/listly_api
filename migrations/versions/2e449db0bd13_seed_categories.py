"""
Seed categories

Revision ID: 2e449db0bd13
Revises: 145155f126e9
Create Date: 2025-03-13 16:29:56.226123

"""
import csv

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic
revision = '2e449db0bd13'
down_revision = '145155f126e9'
branch_labels = None
depends_on = None

CSV_FILE = "seed_data/categories.csv"


def load_seed():
    """Carrega os dados do CSV para uma lista de dicionários."""
    categories = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            categories.append({"id": int(row["id"]), "name": row["name"]})
    return categories


def upgrade():
    """Insere ou atualiza os dados das categorias no banco de dados."""
    conn = op.get_bind()
    categories = load_seed()

    for category in categories:
        conn.execute(
            sa.text(
                """
                INSERT INTO category (id, name) VALUES (:id, :name)
                ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """
            ),
            {"id": category["id"], "name": category["name"]}
        )


def downgrade():
    """Remove os registros inseridos na operação de upgrade."""
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM category WHERE id BETWEEN 1 AND 14;"))
