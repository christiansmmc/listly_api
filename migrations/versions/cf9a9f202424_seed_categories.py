"""Seed categories

Revision ID: cf9a9f202424
Revises: 6a0e771724e9
Create Date: 2025-04-03 11:07:45.522051

"""
import csv

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cf9a9f202424'
down_revision = '6a0e771724e9'
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
    conn = op.get_bind()
    categories = load_seed()

    for category in categories:
        conn.execute(
            sa.text(
                """
                INSERT INTO category (id, name) VALUES (:id, :name)
                ON DUPLICATE KEY UPDATE name = VALUES(name);
                """
            ),
            {"id": category["id"], "name": category["name"]}
        )


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM category WHERE id BETWEEN 1 AND 14;"))
