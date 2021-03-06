"""empty message

Revision ID: ccde635499c4
Revises: b905e88b5cb0
Create Date: 2016-07-04 09:45:11.687369

"""

# revision identifiers, used by Alembic.
revision = 'ccde635499c4'
down_revision = 'b905e88b5cb0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'birth_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'phone',
               existing_type=mysql.VARCHAR(length=14),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=mysql.VARCHAR(length=14),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'birth_date',
               existing_type=sa.DATE(),
               nullable=False)
    ### end Alembic commands ###
