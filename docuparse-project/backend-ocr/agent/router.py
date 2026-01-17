from typing import Dict, Any, List
import time
import logging
from engines.deepseek_engine import DeepSeekEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Capabilities Dictionary
CAPABILITIES = {
    "digital_pdf": ["pdfplumber", "docling"],
    "scanned_image": ["opencv-python", "pytesseract", "easyocr"],
    "handwritten_complex": ["deepseek-ocr", "llama-parse", "unstructured"]
}


def route_and_process(classification: str, content: bytes) -> Dict[str, Any]:
    """
    Selects the tool/engine based on classification and processes the content.
    """
    start_time = time.perf_counter()
    tools_used = []
    data = {}

    try:
        if classification == "digital_pdf":
            # Use PDFPlumber or Docling
            tools_used.extend(CAPABILITIES["digital_pdf"])
            data = _mock_extract(content)

        elif classification == "scanned_image":
            # Use Tesseract or EasyOCR
            tools_used.extend(CAPABILITIES["scanned_image"])
            data = _mock_extract(content)

        elif classification == "handwritten_complex":
            # Use DeepSeek (primary) or fallbacks
            logger.info(
                f"Routing to DeepSeek Engine for classification: {classification}")
            tools_used.append("deepseek-ocr")

            try:
                engine = DeepSeekEngine()
                # DeepSeekEngine expects bytes for image processing since we don't have a file path on disk yet in this flow
                # (or we need to save it temporarily). The engine handles bytes.
                data = engine.process(content)
            except Exception as e:
                logger.error(f"DeepSeek failed: {e}")
                data = _mock_extract(content)  # Fallback
                data["raw_text_fallback"] = f"DeepSeek Error: {e}. Fallback used."

        else:
            tools_used.append("basic_fallback")
            data = _mock_extract(content)

    except Exception as e:
        logger.error(f"Routing error: {e}")
        data = _mock_extract(content)
        data["raw_text_fallback"] = f"Processing Error: {str(e)}"

    end_time = time.perf_counter()
    processing_time = (end_time - start_time) * 1000

    logger.info(
        f"Processed {classification} in {processing_time:.2f}ms using {tools_used}")

    # Standardization
    normalized_data = _normalize_output(data)

    return {
        "tools_used": tools_used,
        "transcription": normalized_data,
        "_meta": {
            "processing_time_ms": processing_time
        }
    }


def _normalize_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures the output follows the strict JSON schema.
    """
    return {
        "document_info": data.get("document_info", {}),
        "entities": data.get("entities", {}),
        "tables": data.get("tables", []),  # Ensure lists
        "totals": data.get("totals", {}),
        "raw_text_fallback": data.get("raw_text_fallback", "")
    }


def _mock_extract(content: bytes) -> Dict[str, Any]:
    return {
        "document_info": {},
        "entities": {},
        "tables": [],
        "totals": {},
        "raw_text_fallback": "Content processed (mock)"
    }
