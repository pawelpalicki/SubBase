import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import USERS # Importujemy słownik USERS z app/__init__.py

# Ten blueprint będzie odwoływał się do szablonów w głównym katalogu 'app/templates'
auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Jeśli użytkownik jest już zalogowany, przekieruj go na stronę główną
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on' # Zaznaczony checkbox

        user = USERS.get(username) # Pobierz użytkownika z naszego słownika

        # Sprawdź, czy użytkownik istnieje i hasło jest poprawne
        if user and user.check_password(password):
            login_user(user, remember=remember_me) # Zaloguj użytkownika
            session.permanent = remember_me # Ustaw sesję jako permanentną jeśli wybrano "Zapamiętaj mnie"
            flash('Zalogowano pomyślnie!', 'success')
            # Przekieruj na stronę, do której użytkownik próbował uzyskać dostęp przed zalogowaniem
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Nieprawidłowy login lub hasło.', 'danger')
    return render_template('login.html')

@auth.route('/logout')
@login_required # Tylko zalogowani użytkownicy mogą się wylogować
def logout():
    # Czyszczenie cache'u specyficznego dla sesji
    session_id = session.get('_id', None)
    if session_id:
        cache_dir = os.path.join(current_app.instance_path, 'cache')
        if os.path.exists(cache_dir):
            for filename in os.listdir(cache_dir):
                if filename.startswith(f"{session_id}_"):
                    try:
                        os.remove(os.path.join(cache_dir, filename))
                    except Exception as e:
                        flash(f"Nie udało się usunąć pliku z cache: {filename}. Błąd: {e}", "warning")

    logout_user() # Wyloguj użytkownika
    flash('Zostałeś wylogowany.', 'info')
    return redirect(url_for('auth.login')) # Przekieruj na stronę logowania