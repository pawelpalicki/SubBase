import os
import sys
from sqlalchemy import text, inspect
from sqlalchemy.exc import ProgrammingError

# Add project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import create_app, db
from app.models import (
    Firmy, FirmyTyp, AdresyTyp, Adresy, EmailTyp, Email, TelefonTyp, Telefon,
    Specjalnosci, Osoby, Oceny, Project, Tender, WorkType, UnitPrice, Category, Powiaty
)

def reset_database_sequences():
    """
    Resets the auto-incrementing sequences for all relevant tables in the database.
    It finds the current max ID for each table and sets the sequence to start
    from the next available ID.
    """
    flask_app = create_app()
    with flask_app.app_context():
        # List of models with integer primary keys that need sequence reset
        models_to_reset = [
            Firmy, FirmyTyp, AdresyTyp, Adresy, EmailTyp, Email, TelefonTyp, Telefon,
            Specjalnosci, Osoby, Oceny, Project, Tender, WorkType, UnitPrice, Category, Powiaty
        ]

        print("Starting sequence reset process...")

        for model in models_to_reset:
            try:
                table_name = model.__tablename__
                
                # Use SQLAlchemy's inspection to find the primary key column
                primary_key_columns = inspect(model).primary_key
                if not primary_key_columns or len(primary_key_columns) > 1:
                    print(f"-> Skipping '{table_name}': No single primary key found.")
                    continue
                
                pk_column = primary_key_columns[0]
                pk_name = pk_column.name

                # Check if the primary key is of integer type
                if not isinstance(pk_column.type, (db.Integer, db.BigInteger)):
                     print(f"-> Skipping '{table_name}': Primary key '{pk_name}' is not an integer type.")
                     continue

                # Standard sequence name convention for PostgreSQL
                sequence_name = f"{table_name}_{pk_name}_seq"

                with db.session.begin_nested():
                    # Get the current maximum value of the primary key
                    max_id_result = db.session.execute(text(f'SELECT MAX({pk_name}) FROM "{table_name}"')).scalar_one_or_none()
                    
                    next_id = 1
                    if max_id_result is not None:
                        next_id = int(max_id_result) + 1

                    # Reset the sequence
                    # The 'IF EXISTS' clause makes it safe for tables that might not have a sequence
                    sql_command = text(f"ALTER SEQUENCE IF EXISTS {sequence_name} RESTART WITH {next_id}")
                    db.session.execute(sql_command)
                    
                    print(f"  - Successfully reset sequence '{sequence_name}' for table '{table_name}'. Next ID will be {next_id}.")

            except ProgrammingError as e:
                # This can happen if a sequence doesn't exist (e.g., for tables without auto-increment)
                # or if the naming convention is different.
                db.session.rollback()
                print(f"  - WARNING: Could not reset sequence for table '{table_name}'.")
                print(f"    Reason: {e.orig}")
            except Exception as e:
                db.session.rollback()
                print(f"  - ERROR: An unexpected error occurred for table '{table_name}': {e}")

        db.session.commit()
        print("\nSequence reset process finished successfully.")

if __name__ == '__main__':
    reset_database_sequences()
