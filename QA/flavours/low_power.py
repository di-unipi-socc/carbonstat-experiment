from flavours.interface import CarbonAwareStrategy
from transformers import pipeline
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Low power strategy
class LowPowerStrategy(CarbonAwareStrategy):

    def nop() -> str:
        return "LOW_POWER"

    def ans(text) -> str:
        pipe = pipeline('question-answering', model="distilbert-base-cased-distilled-squad")
        result = pipe(question="What is this article about?",context=text)
        return result["answer"]