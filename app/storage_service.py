import io
import os
from flask import current_app
from werkzeug.utils import secure_filename

try:
    from google.cloud import storage
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False

class BaseStorageService:
    def upload(self, file_stream, filename, content_type):
        raise NotImplementedError

    def download(self, storage_path):
        raise NotImplementedError

    def delete(self, storage_path):
        raise NotImplementedError

class GcsStorageService(BaseStorageService):
    def __init__(self, bucket_name):
        if not GCS_AVAILABLE:
            raise RuntimeError("Biblioteka google-cloud-storage nie jest zainstalowana.")
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME nie jest skonfigurowany.")
        
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload(self, file_stream, filename, content_type):
        file_stream.seek(0)
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file_stream, content_type=content_type)
        return blob.name

    def download(self, storage_path):
        blob = self.bucket.blob(storage_path)
        return io.BytesIO(blob.download_as_bytes())

    def delete(self, storage_path):
        blob = self.bucket.blob(storage_path)
        if blob.exists():
            blob.delete()
            return True
        return False

class LocalStorageService(BaseStorageService):
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def upload(self, file_stream, filename, content_type=None):
        safe_filename = secure_filename(filename)
        upload_path = os.path.join(self.upload_folder, safe_filename)
        file_stream.seek(0)
        with open(upload_path, 'wb') as f:
            f.write(file_stream.read())
        return upload_path

    def download(self, storage_path):
        return io.BytesIO(open(storage_path, 'rb').read())

    def delete(self, storage_path):
        if os.path.exists(storage_path):
            os.remove(storage_path)
            return True
        return False

_storage_service_instance = None

def get_storage_service():
    global _storage_service_instance
    if _storage_service_instance is None:
        gcs_bucket = current_app.config.get('GCS_BUCKET_NAME')
        
        if gcs_bucket and GCS_AVAILABLE:
            try:
                _storage_service_instance = GcsStorageService(gcs_bucket)
                current_app.logger.info("KONFIGURACJA: Inicjalizuję serwis: Google Cloud Storage.")
            except Exception as e:
                current_app.logger.error(f"BŁĄD: Inicjalizacja GCS nie powiodła się ({e}). Przełączam na tryb lokalny.")
                upload_folder = current_app.config['UPLOAD_FOLDER']
                _storage_service_instance = LocalStorageService(upload_folder)
        else:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            _storage_service_instance = LocalStorageService(upload_folder)
            current_app.logger.info(f"KONFIGURACJA: Inicjalizuję serwis: Lokalny folder ({upload_folder}). GCS nie skonfigurowany.")

    return _storage_service_instance