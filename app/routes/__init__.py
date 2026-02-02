from flask import Blueprint

main = Blueprint('main', __name__)

from . import companies, projects, persons, dictionaries, auth, tenders, general as main_routes