import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Placeholder imports - will be replaced by actual implementations
# from agent.router import route_and_process

app = FastAPI(title="DocuParse OCR Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    # Internal service, but good practice to be explicit if needed
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DocumentInfo(BaseModel):
    type: Optional[str] = None
    number: Optional[str] = None
    date: Optional[str] = None


class Entities(BaseModel):
    issuer: Optional[str] = None
    recipient: Optional[str] = None


class TableRow(BaseModel):
    description: Optional[str] = None
    quantity: Optional[Any] = None
    unit_price: Optional[Any] = None
    total: Optional[Any] = None


class Totals(BaseModel):
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    grand_total: Optional[float] = None


class Transcription(BaseModel):
    document_info: DocumentInfo
    entities: Entities
    tables: List[TableRow]
    totals: Totals
    raw_text_fallback: Optional[str] = None


class OCRResponse(BaseModel):
    filename: str
    detected_type: str
    tools_used: List[str]
    transcription: Transcription
    processing_time_ms: float


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/process", response_model=OCRResponse)
async def process_document(file: UploadFile = File(...)):
    start_time = time.time()

    try:
        contents = await file.read()
        filename = file.filename

        # Call the router
        from agent.classifier import classify_document
        from agent.router import route_and_process

        # 1. Classify
        classification = classify_document(filename, contents)

        # 2. Process
        result = route_and_process(classification, contents)

        processing_time = result.get("_meta", {}).get(
            "processing_time_ms", (time.time() - start_time) * 1000)

        return {
            "filename": filename,
            "detected_type": classification,
            "tools_used": result.get("tools_used", []),
            "transcription": result.get("transcription", {}),
            "processing_time_ms": processing_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
