"""Add Flow model

Revision ID: a54b66335b55
Revises: 51a9f1ab4b8b
Create Date: 2023-08-02 12:32:20.344118

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'a54b66335b55'
down_revision = '51a9f1ab4b8b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'flow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('state', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('flow')
