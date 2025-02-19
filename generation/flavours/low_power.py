from transformers import pipeline
from flavours.interface import CarbonAwareStrategy
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Low power strategy
class LowPowerStrategy(CarbonAwareStrategy):

    def nop() -> str:
        return "LOW_POWER"

    def ans(text) -> str:
        pipe = pipeline('text-generation', model="distilgpt2", max_length=100, truncation=True)
        result = pipe(text)
        return result