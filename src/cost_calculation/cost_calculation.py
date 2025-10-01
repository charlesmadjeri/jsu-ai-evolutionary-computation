from abc import ABC, abstractmethod

class CostCalculation(ABC):
    @abstractmethod
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        raise NotImplementedError