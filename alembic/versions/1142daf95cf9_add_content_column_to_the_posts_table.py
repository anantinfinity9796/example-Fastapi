"""add content column to the posts table

Revision ID: 1142daf95cf9
Revises: 1a99de4c3a78
Create Date: 2022-04-05 16:06:59.390476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1142daf95cf9'
down_revision = '1a99de4c3a78'
branch_labels = None
depends_on = None


def upgrade():
    """ This contains the code to add a content column to the posts table"""
    
    op.add_column('posts', sa.Column('content', sa.String, nullable = False))

    pass


def downgrade():
    """ This contains the code for the dropping the column in the posts table."""

    op.drop_column('posts', 'content')

    pass
