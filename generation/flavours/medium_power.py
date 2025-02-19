from transformers import pipeline
from flavours.interface import CarbonAwareStrategy
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Medium power strategy
class MediumPowerStrategy(CarbonAwareStrategy):

    def nop() -> str:
        return "MEDIUM_POWER"

    def ans(text) -> str:
        pipe = pipeline('text-generation', model="EleutherAI/gpt-neo-1.3B", max_length=100, truncation=True)
        result = pipe(text)
        return result