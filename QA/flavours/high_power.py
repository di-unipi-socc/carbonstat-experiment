from flavours.interface import CarbonAwareStrategy
from transformers import pipeline
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# High power strategy
class HighPowerStrategy(CarbonAwareStrategy):
    
    def nop() -> str:
        return "HIGH_POWER"
    
    def ans(text) -> str:
        pipe = pipeline('question-answering', model="bert-large-uncased-whole-word-masking-finetuned-squad")
        result = pipe(question="What is this article about?",context=text)
        return result["answer"]