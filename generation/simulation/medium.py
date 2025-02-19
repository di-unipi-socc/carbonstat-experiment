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
        pipe = pipeline('text-generation', model="EleutherAI/gpt-neo-1.3B", max_length=100, truncation=True)
        result = pipe(text)
        print(result)
    except FileNotFoundError:
        print(f"Errore nella lettura di '{filename}'.")