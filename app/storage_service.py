import io
from flask import current_app

class StorageService:
    """
    Klasa serwisowa do obsługi operacji na plikach w Google Cloud Storage.
    Inicjalizuje klienta i bucket raz, aby można było go ponownie wykorzystywać.
    """

    def __init__(self, bucket_name):
        # Import jest tutaj, aby uniknąć błędu, gdy biblioteka nie jest zainstalowana
        from google.cloud import storage
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME nie jest skonfigurowany w aplikacji.")
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload(self, file_stream, filename, content_type):
        """Przesyła strumień pliku do GCS."""
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file_stream, content_type=content_type)
        return blob.name

    def download(self, filename):
        """Pobiera plik z GCS jako strumień bajtów w pamięci."""
        blob = self.bucket.blob(filename)
        return io.BytesIO(blob.download_as_bytes())

    def delete(self, filename):
        """Usuwa plik z GCS, jeśli istnieje."""
        blob = self.bucket.blob(filename)
        if blob.exists():
            blob.delete()
            return True
        return False

# Mechanizm "singleton" do przechowywania jednej instancji serwisu dla całej aplikacji.
_storage_service_instance = None

def get_storage_service():
    """Zwraca instancję serwisu storage. Tworzy ją, jeśli jeszcze nie istnieje."""
    global _storage_service_instance
    if _storage_service_instance is None and current_app.config.get('GCS_BUCKET_NAME'):
        _storage_service_instance = StorageService(current_app.config['GCS_BUCKET_NAME'])
    return _storage_service_instance
