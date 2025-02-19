from flavours.interface import CarbonAwareStrategy
from transformers import pipeline
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# High power strategy
class HighPowerStrategy(CarbonAwareStrategy):
    
    def nop() -> str:
        return "HIGH_POWER"
    
    def ans(text) -> str:
        pipe = pipeline('ner', aggregation_strategy="simple", model="Jean-Baptiste/roberta-large-ner-english")
        result = pipe(text)
        return [(entity["entity_group"], entity["word"]) for entity in result]