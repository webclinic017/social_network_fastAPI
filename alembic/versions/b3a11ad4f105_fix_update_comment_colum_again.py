"""fix update comment colum again

Revision ID: b3a11ad4f105
Revises: f2fe91a689fe
Create Date: 2021-11-29 20:26:09.424996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a11ad4f105'
down_revision = 'f2fe91a689fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
     op.alter_column('update_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Column('update_at', sa.TIMESTAMP(timezone=True), nullable=False),
    # ### end Alembic commands ###