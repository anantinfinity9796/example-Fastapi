"""create post table

Revision ID: 1a99de4c3a78
Revises: 
Create Date: 2022-04-05 15:41:39.891425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a99de4c3a78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """ This function is responsible for making the changes in your table schema. """

    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
    sa.Column('title', sa.String, nullable = False))

    pass


def downgrade():
    """ This function is responsible for reversing the changes in your database schema. """

    op.drop_table('posts')

    pass
