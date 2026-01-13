import logging
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from config import Config
from flask_login import LoginManager, UserMixin, current_user # Importy dla Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash # Do haszowania haseł i weryfikacji
from datetime import timedelta # Do ustawiania czasu życia sesji

# Inicjalizacja rozszerzeń
db = SQLAlchemy()
login_manager = LoginManager() # Inicjalizacja LoginManager

# --- Zarządzanie użytkownikami (dla celów demonstracyjnych: hardkodowane dane) ---
# W rzeczywistej aplikacji te dane pochodziłyby z bazy danych lub innego źródła.
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    def get_id(self):
        return str(self.id) # Flask-Login potrzebuje stringa
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Predefiniowani użytkownicy testowi (hasła zostaną zahaszowane przy starcie aplikacji)
USERS = {
    "ptbnickel": User(1, "ptbnickel", generate_password_hash("L@to2025$")),
    "admin": User(2, "admin", generate_password_hash("adminpassword"))
}

# Funkcja ładowana przez Flask-Login, aby pobrać użytkownika na podstawie jego ID sesji
@login_manager.user_loader
def load_user(user_id):
    for user in USERS.values():
        if user.id == int(user_id):
            return user
    return None
# --- Koniec sekcji zarządzania użytkownikami ---

# Filtr Jinja2 (zakładam, że już go masz)
def fix_url_filter(url):
    if not url: return ""
    if not url.startswith(("http://", "https://")): return f"http://{url}"
    return url

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.permanent_session_lifetime = config_class.PERMANENT_SESSION_LIFETIME

    # --- NOWA, NIEZAWODNA LOGIKA TWORZENIA KATALOGU ---
    # Gwarantuje, że katalog /instance/uploads istnieje przy każdym starcie aplikacji.
    # To jest kluczowe dla efemerycznych systemów plików jak na Render.
    import os
    uploads_folder = os.path.join(app.instance_path, 'uploads')
    os.makedirs(uploads_folder, exist_ok=True)
    # --- KONIEC NOWEJ LOGIKI ---

    app.jinja_env.filters['fix_url'] = fix_url_filter
    db.init_app(app) # Inicjalizacja SQLAlchemy

    # Konfiguracja Flask-Login
    login_manager.init_app(app)
    # Strona, na którą użytkownik zostanie przekierowany, jeśli spróbuje dostać się do chronionej trasy bez logowania
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Musisz się zalogować, aby uzyskać dostęp do tej strony."
    login_manager.login_message_category = "warning"
    login_manager.session_protection = "strong"

    @app.before_request
    def log_request_info():
        app.logger.info(f'Method: {request.method} Path: {request.path} User: {current_user}')

    # Obsługa błędów bazy danych (zakładam, że już ją masz)
    @app.errorhandler(OperationalError)
    def handle_database_error(e):
        app.logger.error(f"🚨 BŁĄD BAZY DANYCH 🚨\nŚcieżka: {request.path}\nBłąd: {str(e)}")
        db.session.remove()
        return render_template('database_error.html'), 500

    # Rejestracja blueprintów
    # Zgodnie z Twoim potwierdzeniem: Twój główny blueprint 'main' jest w app/routs.py
    from .main_routes import main # <--- Ten import jest PRAWIDŁOWY dla app/routs.py
    app.register_blueprint(main)

    # Rejestracja nowego blueprintu dla autoryzacji (logowanie/wylogowanie)
    # Ten blueprint będzie w nowym katalogu app/routes/
    from app.routes import auth
    app.register_blueprint(auth)

    # Rejestracja blueprintu dla ofert
    from app.tenders.routes import tenders_bp
    app.register_blueprint(tenders_bp)

    return app