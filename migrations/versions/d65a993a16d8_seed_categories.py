"""seed categories

Revision ID: d65a993a16d8
Revises: 5aef9a8c8f7a
Create Date: 2025-01-20 10:04:59.456526

"""
from alembic import op
import sqlalchemy as sa

import csv

# revision identifiers, used by Alembic.
revision = 'd65a993a16d8'
down_revision = '5aef9a8c8f7a'
branch_labels = None
depends_on = None

CSV_FILE = "seed_data/categories.csv"


def load_seed():
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
                "INSERT INTO category (id, name) VALUES (:id, :name) "
                "ON DUPLICATE KEY UPDATE name = :name"
            ),
            {"id": category["id"], "name": category["name"]}
        )


def downgrade():
    conn = op.get_bind()
    conn.execute("DELETE FROM categories WHERE id BETWEEN 1 AND 14")
