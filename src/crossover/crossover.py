from abc import ABC, abstractmethod

class Crossover(ABC):
    @abstractmethod
    def __init__(self, parents: tuple[list[int], list[int]], crossover_size_rate: float):
        self.parents = parents
        self.crossover_size_rate = crossover_size_rate
    
    @abstractmethod
    def crossover(self) -> tuple[list[int], list[int]]:
        return None
    
    @abstractmethod
    def get_cross_points(self, crossover_size_rate: float, cities_nb: int) -> tuple[int, int]:
        return None
