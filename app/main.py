import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, UploadFile, File
import shutil
from app.pipeline import run_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FinTech Document Parser API"}


@app.post("/parse-document")
async def parse_document(file: UploadFile = File(...)):

    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_pipeline(file_path)

    return result