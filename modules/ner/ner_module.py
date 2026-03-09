import spacy

# Load Trained NER model
nlp = spacy.load("model/model-last")

def extract_entities(text):

    doc = nlp(text)

    entities = {}

    for ent in doc.ents:
        entities[ent.label_] = ent.text

    return entities