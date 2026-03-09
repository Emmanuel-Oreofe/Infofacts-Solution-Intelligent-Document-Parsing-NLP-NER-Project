from modules.ner.ner_module import extract_entities
def run_pipeline(file_path):
    #OCR
    text = run_ocr(file_path)
    #Preprocessing
    clean_text = preprocess_text(text)
    #NER
    entities = extract_entities(clean_text)
    return entities

def run_ocr(file_path):
    return extracted_text

def preprocess_text(text):
    return clean_text

def extract_entities(text):
    return {
        "BANK NAME": "...",
         "ACCOUNT_NUMBER": "...",
         "IFSC_CODE": "...",
         "TRANSACTION_ID": "...",
         "GST_NUMBER": "...",
        "AMOUNT": "...",
        "DATE": "..."
    }
