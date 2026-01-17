# Development Steps

## Phase 1: DeepSeek OCR Integration

1. **Dependency Management**: Added `openai` to `backend-ocr/requirements.txt` to communicate with the local Ollama instance using the OpenAI-compatible API.
2. **Engine Implementation**: Created `DeepSeekEngine` class in `backend-ocr/engines/deepseek_engine.py` which encodes images to base64 and sends them to the local Ollama API (`http://host.docker.internal:11434/v1/chat/completions`).
3. **Router Integration**: Updated `backend-ocr/agent/router.py` to:
    - Include a `CAPABILITIES` dictionary mapping document types to tools.
    - Use `DeepSeekEngine` for `handwritten_complex` documents.
    - Implement a `_normalize_output` function to guarantee consistent JSON structure.
    - Add performance logging using `time.perf_counter()` and `logging`.
4. **Heuristics Improvement**: Updated `backend-ocr/agent/classifier.py` to better detect complex/handwritten documents based on keywords and file extensions.
5. **Documentation**: Created `backend-ocr/README.md` with setup instructions and `backend-ocr/tests/test_ocr_flow.py` with basic flow validation.
6. **Task Completion**: Saved all steps in `docs/dev_steps.md`.
