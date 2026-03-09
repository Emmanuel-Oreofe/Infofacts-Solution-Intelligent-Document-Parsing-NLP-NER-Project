import spacy

# 1. Load the brain we just trained
nlp = spacy.load("./output/model-best")

# 2. Give it a NEW sentence it has NEVER seen before
test_text = "I sent 25000 INR from Axis Bank to account 1122334455 on 2026-05-10."

# 3. Ask the AI to find the entities
doc = nlp(test_text)

print(f"Testing Sentence: {test_text}\n")
print("AI found these labels:")
for ent in doc.ents:
    print(f"Word: {ent.text}  |  Label: {ent.label_}")