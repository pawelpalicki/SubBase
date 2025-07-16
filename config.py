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

    # --- Ulepszona, uniwersalna konfiguracja Google Credentials ---
    # Definiujemy ścieżkę, gdzie Render umieszcza sekretny plik
    RENDER_GCS_SECRET_FILE = '/etc/secrets/gcs_credentials.json'

    # Zmienne, których używa Twój kod
    google_creds_json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    google_creds_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    # Logika priorytetowa:
    # 1. Sprawdź środowisko Render (najbardziej specyficzne)
    if os.path.exists(RENDER_GCS_SECRET_FILE):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = RENDER_GCS_SECRET_FILE
        print(f"KONFIGURACJA: Wykryto środowisko Render. Użyto danych logowania z pliku: {RENDER_GCS_SECRET_FILE}")

    # 2. Sprawdź, czy jest jawnie zdefiniowana ścieżka do pliku (dla lokalnego developmentu)
    elif google_creds_file_path:
        print(f"KONFIGURACJA: Użyto danych logowania Google Cloud z pliku: {google_creds_file_path}")

    # 3. Sprawdź, czy dane są w zmiennej (dla Replit)
    elif google_creds_json_str:
        try:
            # Ta metoda nie jest zalecana, ale zostawiamy ją dla kompatybilności
            json.loads(google_creds_json_str)
            print("KONFIGURACJA: Pomyślnie wczytano dane logowania Google Cloud ze zmiennej środowiskowej (w pamięci).")
        except json.JSONDecodeError:
            print("BŁĄD KONFIGURACJI: Nie udało się sparsować JSON z GOOGLE_APPLICATION_CREDENTIALS_JSON.")

    # 4. Jeśli żadna z powyższych metod nie zadziałała...
    else:
        # ...nie rób nic i zaufaj, że biblioteka Google sama znajdzie dane (np. w Google Cloud IDE).
        print("KONFIGURACJA: Nie znaleziono jawnej konfiguracji GCS. Aplikacja spróbuje użyć Application Default Credentials (ADC).")

    # --- Lokalny fallback ---
    # Katalog 'uploads' jest teraz tworzony w app/__init__.py
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
