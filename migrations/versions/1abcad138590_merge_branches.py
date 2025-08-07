"""Merge branches

Revision ID: 1abcad138590
Revises: a143b97b3348
Create Date: 2025-08-07 13:07:25.393648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1abcad138590'
down_revision: Union[str, Sequence[str], None] = 'a143b97b3348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
