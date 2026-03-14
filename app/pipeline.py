import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.ner.ner_module import extract_entities

def run_pipeline(file_path):
    text = run_ocr(file_path)
    clean_text = preprocess_text(text)
    entities = extract_entities(clean_text)
    return entities

def run_ocr(file_path):
    extracted_text = (
        "ICICI BANK A/C 123456789012 IFSC ICIC0001234 Transfer of ₹5000 on 12-02-2024"
    )
    return extracted_text

def preprocess_text(text):
    clean_text = text.lower().strip()
    return clean_text

def print_entities(entities):
    if not entities:
        print("No entities found.")
        return

    print("Extracted Entities:")
    for label, value in entities.items():
        print(f"- {label}: {value}")

# ---- TEST PIPELINE ----
if __name__ == "__main__":
    print("Pipeline Started")
    entities = run_pipeline("sample_document.pdf")
    print_entities(entities)
    