import os
import json
from datetime import timedelta
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("Brak zmiennej środowiskowej SECRET_KEY. Ustaw ją przed uruchomieniem aplikacji.")

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

    # --- Uproszczona konfiguracja Google Credentials ---
    google_creds_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if google_creds_file_path:
        print(f"KONFIGURACJA: Znaleziono zmienną GOOGLE_APPLICATION_CREDENTIALS. Aplikacja użyje jej do uwierzytelniania.")
    else:
        print("KONFIGURACJA: Nie znaleziono zmiennej GOOGLE_APPLICATION_CREDENTIALS. Aplikacja spróbuje użyć Application Default Credentials (ADC).")

    # --- Lokalny fallback ---
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
