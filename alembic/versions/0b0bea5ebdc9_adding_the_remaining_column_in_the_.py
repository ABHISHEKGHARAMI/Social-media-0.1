"""adding the remaining column in the posts table

Revision ID: 0b0bea5ebdc9
Revises: ea247796c10a
Create Date: 2025-03-18 12:20:58.065749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b0bea5ebdc9'
down_revision: Union[str, None] = 'ea247796c10a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),nullable=True,server_default=sa.text('true')))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
