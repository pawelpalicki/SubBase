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

    # --- Dynamiczna konfiguracja Google Credentials ---
    google_creds_json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    GOOGLE_CREDS_OBJECT = None

    if google_creds_json_str:
        try:
            GOOGLE_CREDS_OBJECT = json.loads(google_creds_json_str)
            print("KONFIGURACJA: Pomyślnie wczytano dane logowania Google Cloud ze zmiennej środowiskowej (w pamięci).")
        except json.JSONDecodeError:
            print("BŁĄD KONFIGURACJI: Nie udało się sparsować JSON z GOOGLE_APPLICATION_CREDENTIALS_JSON.")
    elif os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        # Jeśli zmienna wskazuje na istniejący plik (standardowe podejście dla środowiska lokalnego)
        print(f"KONFIGURACJA: Użyto danych logowania Google Cloud z pliku: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")
    else:
        print("KONFIGURACJA: Brak skonfigurowanych danych logowania Google Cloud. Operacje na GCS będą niedostępne.")

    # --- Lokalny fallback ---
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print(f"KONFIGURACJA: Utworzono katalog na pliki: {UPLOAD_FOLDER}")
