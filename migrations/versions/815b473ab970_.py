"""empty message

Revision ID: 815b473ab970
Revises: dc2740e84001
Create Date: 2020-06-09 16:18:14.558185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815b473ab970'
down_revision = 'dc2740e84001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('history_view',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('story_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['story_id'], ['story.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_storystats_hits', table_name='storystats')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_storystats_hits', 'storystats', ['hits'], unique=False)
    op.drop_table('history_view')
    # ### end Alembic commands ###
