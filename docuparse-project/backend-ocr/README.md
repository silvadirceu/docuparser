# Backend OCR

FastAPI service responsible for document analysis and data extraction using various OCR engines and LLMs.

## Supported Engines
- **DeepSeek OCR (via Ollama)**: For complex/handwritten documents.
- **Tesseract/EasyOCR**: For standard images.
- **PDFPlumber/Docling**: For digital PDFs.

## Configuration
Ensure these environment variables are set in `.env` or your environment:

- `OLLAMA_HOST`: URL of local Ollama instance (default: `http://host.docker.internal:11434/v1`).
- `OLLAMA_MODEL`: Model to use (default: `deepseek-r1`). *Note: Requires a VLM if processing images directly, or logic to handle text extraction.*

## Running Locally

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

## Development
- **Router**: `agent/router.py` handles the logic for selecting the engine.
- **Classifier**: `agent/classifier.py` determines document type.
- **Engines**: Adapters in `engines/` directory.
