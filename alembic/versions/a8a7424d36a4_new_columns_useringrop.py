"""new columns UserInGrop

Revision ID: a8a7424d36a4
Revises: ced6ebfa64fc
Create Date: 2021-12-08 18:57:06.792820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8a7424d36a4'
down_revision = 'ced6ebfa64fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usersInGroups', sa.Column('update_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('usersInGroups', sa.Column('join_ggroup_date', sa.TIMESTAMP(timezone=True),server_default= None, nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usersInGroups', 'join_ggroup_date')
    op.drop_column('usersInGroups', 'update_at')
    # ### end Alembic commands ###