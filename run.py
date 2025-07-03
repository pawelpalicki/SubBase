from dotenv import load_dotenv
load_dotenv() # Wywołanie load_dotenv() musi nastąpić przed importem modułów aplikacji (np. `app`), które zależą od zmiennych środowiskowych.

from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        # Registers all models with SQLAlchemy
        import app.models
    flask_app.run(host='0.0.0.0', port=8080, debug=True)