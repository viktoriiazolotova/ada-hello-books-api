"""empty message

Revision ID: 26eaec72fb4a
Revises: ff800d9b4d86
Create Date: 2022-11-06 19:03:39.092355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26eaec72fb4a'
down_revision = 'ff800d9b4d86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'book', 'author', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'author_id')
    # ### end Alembic commands ###
