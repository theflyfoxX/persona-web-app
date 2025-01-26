"""Initial migration

Revision ID: 3ad0c3e72a51
Revises: 
Create Date: 2025-01-23 20:22:40.649788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3ad0c3e72a51'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the like_count column to the posts table
    op.add_column('posts', sa.Column('like_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    # Remove the like_count column
    op.drop_column('posts', 'like_count')