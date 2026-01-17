import easyocr
from typing import Dict, Any


class EasyOCREngine:
    def __init__(self):
        # self.reader = easyocr.Reader(['en', 'pt'])
        pass

    def process(self, image_data: Any) -> Dict[str, Any]:
        """
        Process image with EasyOCR.
        """
        return {"raw_text": "EasyOCR output placeholder"}
