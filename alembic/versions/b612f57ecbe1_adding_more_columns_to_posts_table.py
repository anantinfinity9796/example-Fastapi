"""adding more columns to posts table

Revision ID: b612f57ecbe1
Revises: 988b0be8d65b
Create Date: 2022-04-05 17:13:15.879419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b612f57ecbe1'
down_revision = '988b0be8d65b'
branch_labels = None
depends_on = None


def upgrade():
    """ Add more columns to the posts table """

    op.add_column('posts', column = sa.Column('published', sa.Boolean(), nullable =  False, server_default  = 'True'))
    op.add_column('posts', column = sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default = sa.text('NOW()'), nullable = False))

    pass


def downgrade():
    """ Drop the columns which were added in the above upgrade operation"""

    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
