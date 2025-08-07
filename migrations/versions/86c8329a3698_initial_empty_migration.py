"""Initial empty migration

Revision ID: 86c8329a3698
Revises: 
Create Date: 2025-07-04 08:16:08.927472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86c8329a3698'
down_revision: Union[str, Sequence[str], None] = '29a820f177d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
