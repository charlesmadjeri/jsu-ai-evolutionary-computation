from abc import ABC, abstractmethod

"""
Abstract solver class - all solvers must inherit from this class.
"""
class Solver(ABC):
    """
    Returns: list of coordinates and the distance traveled
    """
    @abstractmethod
    def solve(self, coordinates: list[tuple[float, float]]) -> tuple[list[tuple[float, float]], float]:
        pass

    def mutate(self) -> bool:
        return False