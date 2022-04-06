"""add user table

Revision ID: 9047a87e3eff
Revises: 1142daf95cf9
Create Date: 2022-04-05 16:34:05.534758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9047a87e3eff'
down_revision = '1142daf95cf9'
branch_labels = None
depends_on = None


def upgrade():
    """ This function will create the table users with its properties """
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(),nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True),
                        server_default = sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),  # Another method to set the primary key
                    sa.UniqueConstraint('email')                
                    )
    pass


def downgrade():
    """ This function drops the users table"""

    op.drop_table('users')
    pass
