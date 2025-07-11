"""empty message

Revision ID: 5e51449d142b
Revises: c801b5b50ecc
Create Date: 2025-07-05 16:24:53.283542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e51449d142b'
down_revision: Union[str, Sequence[str], None] = 'c801b5b50ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('unit_prices', sa.Column('id_work_type', sa.Integer(), nullable=True))
    op.alter_column('unit_prices', 'nazwa_roboty',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.create_foreign_key(None, 'unit_prices', 'work_types', ['id_work_type'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit_prices', type_='foreignkey')
    op.alter_column('unit_prices', 'nazwa_roboty',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('unit_prices', 'id_work_type')
    op.drop_table('work_types')
    # ### end Alembic commands ###