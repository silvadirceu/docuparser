import requests
from django.conf import settings
from typing import Dict, Any


class OCRClient:
    def __init__(self):
        self.base_url = getattr(
            settings, 'BACKEND_OCR_URL', 'http://backend-ocr:8080')

    def process_document(self, file_obj, filename: str) -> Dict[str, Any]:
        """
        Sends the file to backend-ocr for processing.
        """
        url = f"{self.base_url}/process"
        # Simplified mime type
        files = {'file': (filename, file_obj, 'application/pdf')}

        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Log error
            print(f"Error communicating with OCR backend: {e}")
            raise
