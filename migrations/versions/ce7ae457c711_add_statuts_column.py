"""Add statuts column

Revision ID: ce7ae457c711
Revises: c4800e350ac5
Create Date: 2018-07-04 15:21:09.172008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce7ae457c711'
down_revision = 'c4800e350ac5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_request_request'), 'user_request', ['request'], unique=False)
    op.create_index(op.f('ix_user_request_timestamp'), 'user_request', ['timestamp'], unique=False)
    op.drop_index('ix_no_result_user_request_request', table_name='no_result_user_request')
    op.drop_index('ix_no_result_user_request_timestamp', table_name='no_result_user_request')
    op.drop_table('no_result_user_request')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('no_result_user_request',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('request', sa.VARCHAR(length=200), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_no_result_user_request_timestamp', 'no_result_user_request', ['timestamp'], unique=False)
    op.create_index('ix_no_result_user_request_request', 'no_result_user_request', ['request'], unique=False)
    op.drop_index(op.f('ix_user_request_timestamp'), table_name='user_request')
    op.drop_index(op.f('ix_user_request_request'), table_name='user_request')
    op.drop_table('user_request')
    # ### end Alembic commands ###
