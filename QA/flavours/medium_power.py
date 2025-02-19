from flavours.interface import CarbonAwareStrategy
from transformers import pipeline
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Medium power strategy
class MediumPowerStrategy(CarbonAwareStrategy):

    def nop() -> str:
        return "MEDIUM_POWER"

    def ans(text) -> str:
        pipe = pipeline('question-answering', model="deepset/roberta-base-squad2")
        result = pipe(question="What is this article about?",context=text)
        return result["answer"]