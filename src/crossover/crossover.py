from abc import ABC, abstractmethod
import random

class Crossover(ABC):
    @abstractmethod
    def __init__(self, parents: tuple[list[int], list[int]], crossover_size_rate: float):
        self.parents = parents
        self.crossover_size_rate = crossover_size_rate
    
    @abstractmethod
    def crossover(self) -> tuple[list[int], list[int]]:
        return None
    
    @abstractmethod
    def get_cross_points(self, cities_nb) -> tuple[int, int]:
        crossover_lt = (int) (self.crossover_size_rate * cities_nb)
        idx_a = random.randint(0, cities_nb - crossover_lt)
        idx_b = idx_a + crossover_lt
        return (idx_a, idx_b)
