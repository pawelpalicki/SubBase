import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jakis_domyslny_klucz_na_wypadek_braku_env'
    _database_url = os.environ.get('DATABASE_URL')
    if _database_url:
        SQLALCHEMY_DATABASE_URI = _database_url.replace('postgres://', 'postgresql://')
    else:
        # Użyj ścieżki absolutnej, aby uniknąć problemów z katalogiem roboczym
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'firmy.db')

    # --- DEBUGOWANIE ---
    # Poniższa linia wyświetli w konsoli, z którą bazą danych łączy się aplikacja.
    # Jest to przydatne do szybkiego sprawdzenia konfiguracji.
    print(f"✅ KONFIGURACJA: Aplikacja łączy się z bazą -> {SQLALCHEMY_DATABASE_URI}")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 30,
        'max_overflow': 20
    }

    # test