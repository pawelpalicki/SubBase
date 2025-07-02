import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Wczytaj zmienne środowiskowe
load_dotenv()

# Konfiguracja baz danych
POSTGRES_DATABASE_URL = os.environ.get('DATABASE_URL')
if POSTGRES_DATABASE_URL:
    POSTGRES_DATABASE_URL = POSTGRES_DATABASE_URL.replace('postgres://', 'postgresql://')
else:
    print("Brak zmiennej środowiskowej DATABASE_URL. Upewnij się, że jest ustawiona na URL do bazy PostgreSQL.")
    exit()

# Użyj ścieżki absolutnej, aby skrypt działał poprawnie niezależnie od miejsca uruchomienia
basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'firmy.db')

def copy_data():
    postgres_session = None
    sqlite_session = None
    try:
        # Połączenie z bazą PostgreSQL (źródło)
        postgres_engine = create_engine(POSTGRES_DATABASE_URL)
        postgres_metadata = MetaData()
        postgres_metadata.reflect(bind=postgres_engine) # Odczytaj schemat bazy PostgreSQL
        PostgresSession = sessionmaker(bind=postgres_engine)
        postgres_session = PostgresSession()

        # Połączenie z bazą SQLite (cel)
        sqlite_engine = create_engine(SQLITE_DATABASE_URL)
        sqlite_metadata = MetaData()
        
        # Odtwórz schemat bazy PostgreSQL w SQLite
        for table_name in postgres_metadata.tables:
            table = postgres_metadata.tables[table_name]
            table.to_metadata(sqlite_metadata) 
        
        sqlite_metadata.create_all(sqlite_engine) # Utwórz tabele w SQLite

        SqliteSession = sessionmaker(bind=sqlite_engine)
        sqlite_session = SqliteSession()

        # Iteracja przez każdą tabelę i kopiowanie danych
        for table_name in postgres_metadata.tables:
            postgres_table = Table(table_name, postgres_metadata, autoload_with=postgres_engine)
            sqlite_table = Table(table_name, sqlite_metadata, autoload_with=sqlite_engine)

            print(f"Kopiowanie danych z tabeli: {table_name}")
            
            # Pobierz wszystkie dane z tabeli PostgreSQL
            rows = postgres_session.query(postgres_table).all()

            if rows:
                # Wstaw dane do tabeli SQLite
                # Używamy instrukcji insert bezpośrednio na obiekcie Table
                # Zmieniamy row._asdict() na słownik z wartościami kolumn
                data_to_insert = [row._asdict() for row in rows]
                
                # Użyj sqlite_session.execute() z instrukcją insert
                # Tutaj `sqlite_table` to faktyczny obiekt Table, a `data_to_insert` to lista słowników
                sqlite_session.execute(sqlite_table.insert(), data_to_insert)
                
                print(f"Skopiowano {len(data_to_insert)} wierszy do tabeli {table_name} w SQLite.")
            else:
                print(f"Tabela {table_name} w PostgreSQL jest pusta. Brak danych do skopiowania.")

        # Zatwierdź zmiany w bazie SQLite
        sqlite_session.commit()
        print("Dane zostały pomyślnie skopiowane z PostgreSQL do firmy.db!")

    except Exception as e:
        if sqlite_session:
            sqlite_session.rollback() # Cofnij zmiany w przypadku błędu
        print(f"Wystąpił błąd podczas kopiowania danych: {e}")
    finally:
        if postgres_session:
            postgres_session.close()
        if sqlite_session:
            sqlite_session.close()

if __name__ == "__main__":
    copy_data()