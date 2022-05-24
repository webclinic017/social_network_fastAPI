"""new column

Revision ID: 31315922fe84
Revises: de0ddce45e8b
Create Date: 2022-05-04 10:22:15.467246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31315922fe84'
down_revision = 'de0ddce45e8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('JoinRequestGroups', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('JoinRequestGroups', 'name')
    # ### end Alembic commands ###
