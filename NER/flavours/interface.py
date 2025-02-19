from abc import ABC, abstractmethod

# Abstract carbon-aware strategy
class CarbonAwareStrategy(ABC):
    @abstractmethod
    def nop() -> str:
        pass

    @abstractmethod
    def ans(text) -> str:
        pass