import os
import json
from datetime import timedelta
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jakis_domyslny_klucz_na_wypadek_braku_env'

    # --- Konfiguracja bazy danych ---
    _database_url = os.environ.get('DATABASE_URL')
    if _database_url:
        SQLALCHEMY_DATABASE_URI = _database_url.replace('postgres://', 'postgresql://')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'firmy.db')

    print(f"KONFIGURACJA: Aplikacja łączy się z bazą -> {SQLALCHEMY_DATABASE_URI}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 30,
        'max_overflow': 20
    }

    # --- Konfiguracja przechowywania plików ---
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')

    # --- Dynamiczna konfiguracja Google Credentials (z obsługą Render.com) ---
# Definiujemy ścieżkę, gdzie Render umieszcza sekretny plik
RENDER_GCS_SECRET_FILE = '/etc/secrets/gcs_credentials.json'

# Zmienne, których używa Twój kod
google_creds_json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
google_creds_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
GOOGLE_CREDS_OBJECT = None # Ta zmienna może być potrzebna w Twoim kodzie

# Logika priorytetowa:
# 1. Sprawdź środowisko Render
# 2. Sprawdź metodę z Replit (JSON w zmiennej)
# 3. Sprawdź metodę standardową (ścieżka w zmiennej)

if os.path.exists(RENDER_GCS_SECRET_FILE):
    # JESTEŚMY NA RENDER
    # Ustawiamy standardową zmienną Google, aby wskazywała na plik.
    # Biblioteka Google sama go odnajdzie.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = RENDER_GCS_SECRET_FILE
    print(f"KONFIGURACJA: Wykryto środowisko Render. Użyto danych logowania z pliku: {RENDER_GCS_SECRET_FILE}")

elif google_creds_json_str:
    # JESTEŚMY NA REPLIT (lub podobnym środowisku)
    # To jest Twoja dotychczasowa logika dla Replit.
    try:
        GOOGLE_CREDS_OBJECT = json.loads(google_creds_json_str)
        print("KONFIGURACJA: Pomyślnie wczytano dane logowania Google Cloud ze zmiennej środowiskowej (w pamięci).")
    except json.JSONDecodeError:
        print("BŁĄD KONFIGURACJI: Nie udało się sparsować JSON z GOOGLE_APPLICATION_CREDENTIALS_JSON.")
        # Warto tutaj też ustawić GOOGLE_CREDS_OBJECT na None, żeby uniknąć problemów
        GOOGLE_CREDS_OBJECT = None

elif google_creds_file_path:
    # JESTEŠMY LOKALNIE (lub w innym standardowym środowisku)
    # To jest Twoja dotychczasowa logika dla pliku.
    print(f"KONFIGURACJA: Użyto danych logowania Google Cloud z pliku: {google_creds_file_path}")

else:
    # BRAK KONFIGURACJI
    print("KONFIGURACJA: Brak skonfigurowanych danych logowania Google Cloud. Operacje na GCS będą niedostępne.")

    # --- Lokalny fallback ---
    # Katalog 'uploads' jest teraz tworzony w app/__init__.py
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
