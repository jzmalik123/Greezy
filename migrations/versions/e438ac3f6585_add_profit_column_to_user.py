"""Add Profit Column to user

Revision ID: e438ac3f6585
Revises: c357b44aa307
Create Date: 2022-03-12 20:05:42.633917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e438ac3f6585'
down_revision = 'c357b44aa307'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profit', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profit')
    # ### end Alembic commands ###