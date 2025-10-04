from abc import ABC, abstractmethod

class StopCriterion(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def check(self, total_distance: float):
        pass

    @abstractmethod
    def __str__(self):
        pass