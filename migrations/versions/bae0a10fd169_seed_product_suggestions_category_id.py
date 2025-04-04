"""Seed product suggestions category id

Revision ID: bae0a10fd169
Revises: 18a6682fd2d5
Create Date: 2025-04-04 10:47:49.024327

"""
import csv

import sqlalchemy as sa
from alembic import op

from flaskr.models import normalize_text

CSV_FILE = "seed_data/product_suggestions.csv"

# revision identifiers, used by Alembic.
revision = 'bae0a10fd169'
down_revision = '18a6682fd2d5'
branch_labels = None
depends_on = None


def load_seed():
    products = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            products.append({
                "id": int(row["id"]),
                "name": name,
                "normalized_name": normalize_text(name),
                "category_id": int(row["category_id"]) if row["category_id"] else None
            })
    return products


def upgrade():
    conn = op.get_bind()
    products = load_seed()

    for product in products:
        conn.execute(
            sa.text(
                """
                UPDATE product_suggestion
                SET category_id = :category_id
                WHERE id = :id
                """
            ),
            {
                "id": product["id"],
                "category_id": product["category_id"]
            }
        )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE product_suggestion SET category_id = NULL;"))
