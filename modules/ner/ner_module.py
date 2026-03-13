import spacy

from pathlib import Path
MODEL_DIR = Path(__file__).resolve().parents[2] / "model" / "model-last"
if not MODEL_DIR.exists():
    raise FileNotFoundError(
        f"spaCy model directory not found at: {MODEL_DIR}. "
        "Train/export the model to model/model-last before running the pipeline."
    )

# Load Trained NER model from an absolute path so CWD does not matter.
nlp = spacy.load(MODEL_DIR.as_posix())

def extract_entities(text):
    doc = nlp(text)
    entities = {}

    for ent in doc.ents:
        entities[ent.label_] = ent.text
    return entities
