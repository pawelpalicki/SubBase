"""Add extracted_content to Tender

Revision ID: b55f030d6244
Revises: a143b97b3348
Create Date: 2025-10-04 13:40:47.990704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b55f030d6244'
down_revision: Union[str, Sequence[str], None] = 'a143b97b3348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tenders', sa.Column('extracted_content', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tenders', 'extracted_content')
