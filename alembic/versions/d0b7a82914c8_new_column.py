"""new column

Revision ID: d0b7a82914c8
Revises: 31315922fe84
Create Date: 2022-06-03 16:12:23.745063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b7a82914c8'
down_revision = '31315922fe84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('JoinRequestGroups', sa.Column('group_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('JoinRequestGroups', 'group_name')
    # ### end Alembic commands ###