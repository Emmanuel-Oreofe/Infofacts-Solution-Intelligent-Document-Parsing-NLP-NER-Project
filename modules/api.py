import json
import logging
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from nlp_module import FinancialEntityExtractor
from ocr_module import OCRProcessor
from utils import clean_text, setup_logging

setup_logging("INFO")
logger = logging.getLogger("api")

app = FastAPI(title="FinTech Intelligent Document Parser", version="1.0.0")
ocr = OCRProcessor()
nlp = FinancialEntityExtractor()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/parse")
async def parse_document(file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        ocr_result = ocr.extract_text(tmp_path)
        cleaned_text = clean_text(ocr_result["raw_text"])
        entities = nlp.extract_entities(cleaned_text)

        return {
            "file_name": file.filename,
            "file_type": ocr_result["file_type"],
            "entities": entities,
            "clean_text": cleaned_text,
        }
    except Exception as exc:
        logger.exception("Failed to parse uploaded document")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass


@app.get("/")
def root() -> dict:
    return {"service": "FinTech Intelligent Document Parser", "docs": "/docs"}
