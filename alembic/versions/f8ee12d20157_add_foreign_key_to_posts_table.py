"""add foreign-key to posts table

Revision ID: f8ee12d20157
Revises: 12fe029305be
Create Date: 2024-02-13 12:44:28.657799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f8ee12d20157'
down_revision: Union[str, None] = '12fe029305be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
