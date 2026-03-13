import re
import spacy
from datetime import datetime
from modules.app import fix_ocr_errors

nlp = spacy.load("en_core_web_sm")

def clean_text(text):  # Clean Text
 
    text = re.sub(r"[^a-zA-Z0-9./:₹Rs ]", " ", text)  # Remove unwanted characters

    text = re.sub(r"\s+", " ", text)   # Remove extra spaces

    return text.strip()


def normalize_date(text):  # Normalize Date

    match = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", text)

    if match:
        raw_date = match.group()

        try:
            date_obj = datetime.strptime(raw_date, "%d/%m/%Y")
        except:
            date_obj = datetime.strptime(raw_date, "%d-%m-%Y")

        return date_obj.strftime("%Y-%m-%d")

    return None

def tokenize_text(text):  #  Tokenization + Stopword Removal + Lemmatization

    doc = nlp(text)

    tokens = []

    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.lemma_.lower())

    return tokens

def preprocess_text(text): #preproccessing


    text = fix_ocr_errors(text)
    text = clean_text(text)

    tokens = tokenize_text(text)

    date = normalize_date(text)

    return {
        "clean_text": text,
        "tokens": tokens,
        "date": date
    }