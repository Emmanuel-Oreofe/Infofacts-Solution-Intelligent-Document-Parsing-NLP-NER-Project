import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")
db = DocBin()

with open("data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        text = data['text']
        
        # This part prevents the KeyError:
        labels = data.get('label', []) 
        
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

db.to_disk("./train.spacy")
print("Success! 'train.spacy' has been created.")