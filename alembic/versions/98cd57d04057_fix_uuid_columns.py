"""Fix UUID columns

Revision ID: 98cd57d04057
Revises: c73a8676f1c5
Create Date: 2025-01-27 23:33:24.453974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '98cd57d04057'
down_revision: Union[str, None] = 'c73a8676f1c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('posts',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('like_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='posts_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    postgresql_ignore_search_path=False
    )
  
    op.create_table('likes',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='likes_post_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='likes_pkey')
    )
    # ### end Alembic commands ###



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   pass