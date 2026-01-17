def classify_document(filename: str, content: bytes) -> str:
    """
    Classifies the document into textual_pdf, scanned_image, or handwritten_complex.

    Args:
        filename: Name of the file.
        content: Byte content of the file.

    Returns:
        String indicating the document category.
    """
    filename_lower = filename.lower()

    # 1. Digital PDF (Textual)
    if filename_lower.endswith(".pdf"):
        # Heuristic: If filename suggests scan/invoice without explicitly saying "digital",
        # we might want to check deeper. But for now request says:
        # "PDF Digital (Text Layer): Usar pdfplumber..."
        # We assume standard PDFs are digital unless marked otherwise.
        return "digital_pdf"

    # 2. Handwritten/Complex
    # Check for keywords that might indicate complex docs or explicit user override
    if "manuscrito" in filename_lower or "complex" in filename_lower or "handwritten" in filename_lower:
        return "handwritten_complex"

    # 3. Scanned Image
    if filename_lower.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
        return "scanned_image"

    return "unknown"
