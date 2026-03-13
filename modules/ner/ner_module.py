import re
from typing import Dict
try:
    import spacy
except ModuleNotFoundError:  # pragma: no cover - depends on environment
    spacy = None
def _regex_fallback_entities(text: str) -> Dict[str, str]:
    """Fallback extractor when spaCy/model is unavailable or returns no entities."""
    entities: Dict[str, str] = {}

    amount_match = re.search(r"(?:₹|RS\.?\s?)([\d,]+(?:\.\d+)?)", text, flags=re.IGNORECASE)
    if amount_match:
        entities["AMOUNT"] = amount_match.group(1).replace(",", "")

    date_match = re.search(r"\b\d{2}[-/]\d{2}[-/]\d{4}\b", text)
    if date_match:
        entities["DATE"] = date_match.group(0)

    account_match = re.search(r"\b\d{9,18}\b", text)
    if account_match:
        entities["ACCOUNT_NO"] = account_match.group(0)

    ifsc_match = re.search(r"\b[A-Z]{4}0[A-Z0-9]{6}\b", text, flags=re.IGNORECASE)
    if ifsc_match:
        entities["IFSC"] = ifsc_match.group(0).upper()

    return entities

def _load_model():
    if spacy is None:
        return None
    try:
        model = spacy.load("model/model-last")
    except Exception:
        return None
    return model


nlp = _load_model()


def extract_entities(text: str) -> Dict[str, str]:
    if nlp is None:
        return _regex_fallback_entities(text)

    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}

    if entities:
        return entities
    return _regex_fallback_entities(text)