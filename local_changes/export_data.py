'''
Skrypt do eksportu danych z bazy danych do plików CSV.

Ten skrypt wykorzystuje kontekst aplikacji Flask do połączenia się z bazą danych,
a następnie używa biblioteki pandas do wyeksportowania każdej zdefiniowanej tabeli
do osobnego pliku CSV w podkatalogu 'data_export'.
'''

import os
import pandas as pd
from flask import Flask
from config import Config
from app import db
from app.models import (
    Firmy, FirmyTyp, AdresyTyp, Adresy, EmailTyp, Email, TelefonTyp, Telefon,
    Specjalnosci, FirmySpecjalnosci, Kraj, Wojewodztwa, Powiaty, FirmyObszarDzialania,
    Osoby, Oceny, Project, Tender, WorkType, UnitPrice, Category
)

# --- Minimalna inicjalizacja aplikacji Flask ---
# Tworzymy instancję aplikacji i ładujemy konfigurację, ale NIE REJESTRUJEMY tras (blueprintów).
# To pozwala uzyskać dostęp do bazy danych z pominięciem części aplikacji, które mogą
# zawierać błędy importu (jak np. google.cloud.vision) i nie są potrzebne do eksportu.
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
# --- Koniec minimalnej inicjalizacji ---

# Nazwa katalogu, do którego zostaną wyeksportowane pliki CSV
EXPORT_DIR = 'data_export'

# Lista modeli do wyeksportowania
MODELS_TO_EXPORT = [
    Firmy, FirmyTyp, AdresyTyp, Adresy, EmailTyp, Email, TelefonTyp, Telefon,
    Specjalnosci, FirmySpecjalnosci, Kraj, Wojewodztwa, Powiaty, FirmyObszarDzialania,
    Osoby, Oceny, Project, Tender, WorkType, UnitPrice, Category
]

def export_data():
    '''Główna funkcja eksportująca dane.'''
    # Użyj kontekstu aplikacji, aby zapewnić prawidłowe połączenie z bazą danych
    with app.app_context():
        # Sprawdź, czy katalog docelowy istnieje, jeśli nie, utwórz go
        if not os.path.exists(EXPORT_DIR):
            os.makedirs(EXPORT_DIR)
            print(f"Utworzono katalog: {EXPORT_DIR}")

        print("Rozpoczynanie eksportu danych...")

        # Iteruj przez listę modeli
        for model in MODELS_TO_EXPORT:
            table_name = model.__tablename__
            try:
                # Zbuduj zapytanie SQLAlchemy dla danego modelu
                query = db.session.query(model)
                
                # Użyj pandas do wykonania zapytania i wczytania danych do DataFrame
                df = pd.read_sql(query.statement, db.engine)
                
                # Zdefiniuj ścieżkę do pliku CSV
                output_path = os.path.join(EXPORT_DIR, f"{table_name}.csv")
                
                # Zapisz DataFrame do pliku CSV, bez indeksu pandas
                df.to_csv(output_path, index=False, encoding='utf-8')
                
                print(f"Pomyślnie wyeksportowano tabelę '{table_name}' do pliku {output_path}")

            except Exception as e:
                print(f"Wystąpił błąd podczas eksportu tabeli '{table_name}': {e}")

        print("Eksport danych zakończony.")

if __name__ == '__main__':
    export_data()
