""""Add_category_to_WorkType_and_update_relationships"

Revision ID: 6d0c856eb635
Revises: 5e51449d142b
Create Date: 2025-07-06 14:57:58.296307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d0c856eb635'
down_revision: Union[str, Sequence[str], None] = '5e51449d142b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add the id_kategorii column, allowing NULLs temporarily
    op.add_column('work_types', sa.Column('id_kategorii', sa.Integer(), nullable=True))

    # Step 2: Create a default category if it doesn't exist
    op.execute("INSERT INTO categories (nazwa_kategorii) SELECT 'Ogólne' WHERE NOT EXISTS (SELECT 1 FROM categories WHERE nazwa_kategorii = 'Ogólne')")

    # Step 3: Get the ID of the default category
    # This is a bit tricky in a migration, so we'll use a subquery
    op.execute("UPDATE work_types SET id_kategorii = (SELECT id FROM categories WHERE nazwa_kategorii = 'Ogólne') WHERE id_kategorii IS NULL")

    # Step 4: Add the foreign key constraint
    op.create_foreign_key('fk_work_types_category_id', 'work_types', 'categories', ['id_kategorii'], ['id'])

    # Step 5: Now that all rows have a value, alter the column to be NOT NULL
    op.alter_column('work_types', 'id_kategorii', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'work_types', type_='foreignkey')
    op.drop_column('work_types', 'id_kategorii')
    op.alter_column('unit_prices', 'id_work_type',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('telefon_typ', 'id_telefon_typ',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('telefon', 'id_telefon',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('specjalnosci', 'id_specjalnosci',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('osoby', 'id_osoby',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('oceny', 'oceny_id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('firmy_typ', 'id_firmy_typ',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('firmy', 'id_firmy',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('email_typ', 'id_email_typ',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('email', 'id_email',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('adresy_typ', 'id_adresy_typ',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('adresy', 'id_adresy',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
