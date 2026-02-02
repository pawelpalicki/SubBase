"""Add performance indexes on FK columns

Revision ID: perf_indexes_fk
Revises: b55f030d6244
Create Date: 2026-02-02 20:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'perf_indexes_fk'
down_revision = 'b55f030d6244'
branch_labels = None
depends_on = None


def upgrade():
    """Dodaje indeksy na kolumnach FK dla przyspieszenia zapytań."""
    # Indeksy dla tabeli adresy
    op.create_index('ix_adresy_id_firmy', 'adresy', ['id_firmy'], unique=False)
    
    # Indeksy dla tabeli email
    op.create_index('ix_email_id_firmy', 'email', ['id_firmy'], unique=False)
    
    # Indeksy dla tabeli telefon
    op.create_index('ix_telefon_id_firmy', 'telefon', ['id_firmy'], unique=False)
    
    # Indeksy dla tabeli osoby
    op.create_index('ix_osoby_id_firmy', 'osoby', ['id_firmy'], unique=False)
    
    # Indeksy dla tabeli oceny
    op.create_index('ix_oceny_id_firmy', 'oceny', ['id_firmy'], unique=False)
    
    # Indeksy dla tabeli tenders
    op.create_index('ix_tenders_id_firmy', 'tenders', ['id_firmy'], unique=False)
    op.create_index('ix_tenders_id_projektu', 'tenders', ['id_projektu'], unique=False)
    
    # Indeksy dla tabeli unit_prices
    op.create_index('ix_unit_prices_id_oferty', 'unit_prices', ['id_oferty'], unique=False)
    op.create_index('ix_unit_prices_id_work_type', 'unit_prices', ['id_work_type'], unique=False)
    op.create_index('ix_unit_prices_id_kategorii', 'unit_prices', ['id_kategorii'], unique=False)
    
    # Indeksy dla tabeli work_types
    op.create_index('ix_work_types_id_kategorii', 'work_types', ['id_kategorii'], unique=False)


def downgrade():
    """Usuwa indeksy wydajnościowe."""
    op.drop_index('ix_adresy_id_firmy', table_name='adresy')
    op.drop_index('ix_email_id_firmy', table_name='email')
    op.drop_index('ix_telefon_id_firmy', table_name='telefon')
    op.drop_index('ix_osoby_id_firmy', table_name='osoby')
    op.drop_index('ix_oceny_id_firmy', table_name='oceny')
    op.drop_index('ix_tenders_id_firmy', table_name='tenders')
    op.drop_index('ix_tenders_id_projektu', table_name='tenders')
    op.drop_index('ix_unit_prices_id_oferty', table_name='unit_prices')
    op.drop_index('ix_unit_prices_id_work_type', table_name='unit_prices')
    op.drop_index('ix_unit_prices_id_kategorii', table_name='unit_prices')
    op.drop_index('ix_work_types_id_kategorii', table_name='work_types')
