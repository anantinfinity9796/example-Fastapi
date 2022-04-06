"""add foreign key to posts table

Revision ID: 988b0be8d65b
Revises: 9047a87e3eff
Create Date: 2022-04-05 16:54:45.587800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '988b0be8d65b'
down_revision = '9047a87e3eff'
branch_labels = None
depends_on = None


def upgrade():
    """ This will add the owner_id column to the posts table and set up the foreign keys"""

    op.add_column('posts', column = sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_user_fk', source_table = 'posts', referent_table = "users", local_cols = ['owner_id'], remote_cols = ['id'],
                            ondelete= "CASCADE")
    pass


def downgrade():
    "This function would remove the foreign key and drop the owner_id column."

    op.drop_constraint('posts_users_fk', table_name = "posts")
    op.drop_column('posts', 'owner_id')


    pass
