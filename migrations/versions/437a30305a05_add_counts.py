"""add counts

Revision ID: 437a30305a05
Revises: e5b065fca410
Create Date: 2020-08-13 04:04:37.596382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '437a30305a05'
down_revision = 'e5b065fca410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('followers_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('followings_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('mutuals_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'mutuals_count')
    op.drop_column('user', 'followings_count')
    op.drop_column('user', 'followers_count')
    # ### end Alembic commands ###