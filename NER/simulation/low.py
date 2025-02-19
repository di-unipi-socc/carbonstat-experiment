from transformers import pipeline
import warnings
import sys
warnings.simplefilter(action='ignore', category=FutureWarning)
if len(sys.argv) < 2:
    print("Uso: medium.py inputfile")
else:
    filename=sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text=file.read()
        pipe = pipeline('ner', aggregation_strategy="simple", model="dslim/bert-base-NER")
        result = pipe(text)
        print([(entity["entity_group"], entity["word"]) for entity in result])
    except FileNotFoundError:
        print(f"Errore nella lettura di '{filename}'.")