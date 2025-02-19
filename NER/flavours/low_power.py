from flavours.interface import CarbonAwareStrategy
from transformers import pipeline
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Low power strategy
class LowPowerStrategy(CarbonAwareStrategy):

    def nop() -> str:
        return "LOW_POWER"

    def ans(text) -> str:
        pipe = pipeline('ner', aggregation_strategy="simple", model="dslim/bert-base-NER")
        result = pipe(text)
        return [(entity["entity_group"], entity["word"]) for entity in result]