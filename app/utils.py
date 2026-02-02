import re
from app.models import Firmy

from unidecode import unidecode

def normalize_text(text):
    if text is None:
        return ""
    text = str(text)
    normalized = unidecode(text).lower()
    return ''.join(c for c in normalized if c.isalnum() or c.isspace())

def check_company_name(normalized_name):
    # Pobieramy wszystkie nazwy firm z bazy
    companies = Firmy.query.all()
    for company in companies:
        if normalize_text(company.nazwa_firmy) == normalized_name:
            return True, company.nazwa_firmy  # Zwracamy True i oryginalną nazwę znalezionej firmy
    return False, None

def fix_url_filter(url):
    if not url: return ""
    if not url.startswith(("http://", "https://")): return f"http://{url}"
    return url
