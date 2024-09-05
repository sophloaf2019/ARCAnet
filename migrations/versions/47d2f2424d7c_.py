"""empty message

Revision ID: 47d2f2424d7c
Revises: 65f34c35c299
Create Date: 2024-09-04 21:26:36.823925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d2f2424d7c'
down_revision = '65f34c35c299'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assignment', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('assignment')

    # ### end Alembic commands ###
