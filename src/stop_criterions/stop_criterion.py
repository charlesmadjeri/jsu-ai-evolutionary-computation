from abc import ABC, abstractmethod

class StopCriterion(ABC):
    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def check_continue(self, total_distance: float) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass