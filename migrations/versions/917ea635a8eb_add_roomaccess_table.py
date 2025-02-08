"""Add RoomAccess table

Revision ID: 917ea635a8eb
Revises: d65a993a16d8
Create Date: 2025-02-02 12:13:13.442972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '917ea635a8eb'
down_revision = 'd65a993a16d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room_access',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_code', sa.String(length=6), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_access')
    # ### end Alembic commands ###
