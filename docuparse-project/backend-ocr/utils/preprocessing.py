import cv2
import numpy as np
from typing import Any


def preprocess_image(image_bytes: Any) -> np.ndarray:
    """
    Apply standard preprocessing for OCR: grayscale, thresholding, denoising.
    """
    # Placeholder
    # nparr = np.frombuffer(image_bytes, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.array([])
