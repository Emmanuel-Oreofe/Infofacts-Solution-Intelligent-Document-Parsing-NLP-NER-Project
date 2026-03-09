import spacy

nlp = spacy.load("model/model-last")

text = "Transfer of 45000 from account 12345678 on 12/03/2024 at HDFC Bank"

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)