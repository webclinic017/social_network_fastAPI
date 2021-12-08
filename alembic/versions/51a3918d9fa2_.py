"""

Revision ID: 51a3918d9fa2
Revises: 9ed2eda362ae
Create Date: 2021-11-29 20:50:39.307995

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '51a3918d9fa2'
down_revision = '9ed2eda362ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'update_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               server_default=sa.text('now()'), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'update_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###