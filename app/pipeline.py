import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.ner.ner_module import extract_entities
from modules.ocr.ocr_module import run_ocr
from modules.preprocessing.preprocessing_module import preprocess_text

def run_pipeline(file_path):
    """Run OCR -> preprocessing -> NER extraction pipeline for a document."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    raw_text = run_ocr(str(file_path))
    preprocessed = preprocess_text(raw_text)

    entities = extract_entities(preprocessed["clean_text"])
    return {
        "file_path": str(file_path),
        "raw_text": raw_text,
        "clean_text": preprocessed["clean_text"],
        "tokens": preprocessed["tokens"],
        "normalized_date": preprocessed["date"],
        "entities": entities,
    }

def print_entities(result):
    entities = result.get("entities", {})
    if not entities:
        print("No entities found.")
        return
    
    print("Extracted Entities:")
    for label, value in entities.items():
        print(f"- {label}: {value}")
    
    # ---- TEST PIPELINE ----
if __name__ == "__main__":
    print("Pipeline Started")

 # Replace with your actual input file path (.pdf/.png/.jpg etc.)
    sample_file = "sample_document.pdf"
    pipeline_result = run_pipeline(sample_file)

print_entities(pipeline_result)