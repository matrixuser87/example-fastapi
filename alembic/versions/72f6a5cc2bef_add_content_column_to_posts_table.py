"""add content column to posts table


Revision ID: 72f6a5cc2bef
Revises: 76f5bdb26bf8
Create Date: 2024-02-13 12:33:25.108123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72f6a5cc2bef'
down_revision: Union[str, None] = '76f5bdb26bf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
