import io
import os
from flask import current_app
from werkzeug.utils import secure_filename

# Użycie try-except na poziomie modułu jest bardziej standardowe
try:
    from google.cloud import storage
    from google.oauth2 import service_account
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False

class BaseStorageService:
    """Klasa bazowa definiująca interfejs (nie jest to konieczne, ale pomaga w czytelności)."""
    def upload(self, file_stream, filename, content_type):
        raise NotImplementedError

    def download(self, storage_path):
        raise NotImplementedError

    def delete(self, storage_path):
        raise NotImplementedError

class GcsStorageService(BaseStorageService):
    """Klasa do obsługi operacji na plikach w Google Cloud Storage."""
    def __init__(self, bucket_name, credentials=None):
        if not GCS_AVAILABLE:
            raise RuntimeError("Biblioteka google-cloud-storage nie jest zainstalowana.")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME nie jest skonfigurowany.")
        
        if credentials:
            # Inicjalizacja z obiektu w pamięci
            creds = service_account.Credentials.from_service_account_info(credentials)
            self.client = storage.Client(credentials=creds)
        else:
            # Standardowa inicjalizacja (z pliku wskazywanego przez zmienną środowiskową)
            self.client = storage.Client()

        self.bucket = self.client.bucket(bucket_name)

    def upload(self, file_stream, filename, content_type):
        """Przesyła strumień pliku do GCS. Zwraca nazwę pliku (storage_path)."""
        file_stream.seek(0)
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file_stream, content_type=content_type)
        return blob.name

    def download(self, storage_path):
        """Pobiera plik z GCS jako strumień bajtów."""
        blob = self.bucket.blob(storage_path)
        return io.BytesIO(blob.download_as_bytes())

    def delete(self, storage_path):
        """Usuwa plik z GCS."""
        blob = self.bucket.blob(storage_path)
        if blob.exists():
            blob.delete()
            return True
        return False

class LocalStorageService(BaseStorageService):
    """Klasa do obsługi operacji na plikach lokalnie."""
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def upload(self, file_stream, filename, content_type=None):
        """Zapisuje plik na dysku. Zwraca pełną ścieżkę (storage_path)."""
        safe_filename = secure_filename(filename)
        upload_path = os.path.join(self.upload_folder, safe_filename)
        file_stream.seek(0)
        with open(upload_path, 'wb') as f:
            f.write(file_stream.read())
        return upload_path

    def download(self, storage_path):
        """Pobiera plik z dysku jako strumień bajtów."""
        return io.BytesIO(open(storage_path, 'rb').read())

    def delete(self, storage_path):
        """Usuwa plik z dysku."""
        if os.path.exists(storage_path):
            os.remove(storage_path)
            return True
        return False

# Mechanizm "singleton" do przechowywania jednej instancji serwisu
_storage_service_instance = None

def get_storage_service():
    """
    Zwraca odpowiednią instancję serwisu storage (GCS lub lokalną).
    Decyzja jest podejmowana na podstawie konfiguracji aplikacji.
    """
    global _storage_service_instance
    if _storage_service_instance is None:
        gcs_bucket = current_app.config.get('GCS_BUCKET_NAME')
        
        # Uproszczona i bardziej niezawodna logika:
        # Jeśli nazwa bucketu GCS jest zdefiniowana i biblioteka jest dostępna,
        # ZAWSZE próbuj użyć Google Cloud Storage.
        if gcs_bucket and GCS_AVAILABLE:
            try:
                # Próba inicjalizacji. To tutaj biblioteka Google sama szuka
                # danych logowania (zmiennych, ADC, itp.)
                creds_object = current_app.config.get('GOOGLE_CREDS_OBJECT') # Dla kompatybilności z Replit
                _storage_service_instance = GcsStorageService(gcs_bucket, credentials=creds_object)
                current_app.logger.info("KONFIGURACJA: Inicjalizuję serwis: Google Cloud Storage.")
            except Exception as e:
                # Jeśli inicjalizacja GCS się nie powiedzie z jakiegokolwiek powodu
                # (np. brak uprawnień, błąd sieci), przełącz się na tryb lokalny.
                current_app.logger.error(f"BŁĄD: Inicjalizacja GCS nie powiodła się ({e}). Przełączam na tryb lokalny.")
                upload_folder = current_app.config['UPLOAD_FOLDER']
                _storage_service_instance = LocalStorageService(upload_folder)
        else:
            # Jeśli bucket nie jest zdefiniowany, od razu użyj trybu lokalnego.
            upload_folder = current_app.config['UPLOAD_FOLDER']
            _storage_service_instance = LocalStorageService(upload_folder)
            current_app.logger.info(f"KONFIGURACJA: Inicjalizuję serwis: Lokalny folder ({upload_folder}). GCS nie skonfigurowany.")

    return _storage_service_instance