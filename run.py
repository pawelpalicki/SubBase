#!/home/pawelpalicki/projects/SubBase/venv/bin/python
import os
from dotenv import load_dotenv

# Set the project base directory
project_folder = os.path.expanduser('~/projects/SubBase')
load_dotenv(os.path.join(project_folder, '.env'))

from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        # Registers all models with SQLAlchemy
        import app.models
    is_debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    flask_app.run(host='0.0.0.0', port=8080, debug=is_debug_mode)
