from transformers import pipeline
import warnings
import sys
warnings.simplefilter(action='ignore', category=FutureWarning)
if len(sys.argv) < 2:
    print("Uso: low.py inputfile")
else:
    filename=sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text=file.read()
        pipe = pipeline('question-answering', model="distilbert-base-cased-distilled-squad")
        result = pipe(question="What is this article about?",context=text)
        print(result["answer"])
    except FileNotFoundError:
        print(f"Errore nella lettura di '{filename}'.")