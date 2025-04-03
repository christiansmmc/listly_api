"""Seed product suggestions

Revision ID: 709836b5f9c3
Revises: cf9a9f202424
Create Date: 2025-04-03 11:07:58.952621

"""
import csv

import sqlalchemy as sa
from alembic import op

from flaskr.models import normalize_text

# revision identifiers, used by Alembic.
revision = '709836b5f9c3'
down_revision = 'cf9a9f202424'
branch_labels = None
depends_on = None

CSV_FILE = "seed_data/product_suggestions.csv"


def load_seed():
    """Carrega os dados do CSV para uma lista de dicionários."""
    products = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            products.append({
                "id": int(row["id"]),
                "name": name,
                "normalized_name": normalize_text(name)
            })
    return products


def upgrade():
    conn = op.get_bind()
    products = load_seed()

    for product in products:
        conn.execute(
            sa.text(
                """
                INSERT INTO product_suggestion (id, name, normalized_name)
                VALUES (:id, :name, :normalized_name)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    normalized_name = VALUES(normalized_name);
                """
            ),
            {
                "id": product["id"],
                "name": product["name"],
                "normalized_name": product["normalized_name"]
            }
        )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM product_suggestion WHERE id BETWEEN 1 AND 100;"))
