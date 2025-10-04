from abc import ABC, abstractmethod
from random import randint

class Crossover(ABC):
    @abstractmethod
    def __init__(self, segment_length: int | None):
        self.segment_length = segment_length
        if segment_length is None:
            self.get_segment_length = lambda l: randint(1, l - 1)
        else:
            self.get_segment_length = lambda l: self.segment_length

    @abstractmethod
    def crossover(self, parents: tuple[list[int], list[int]]) -> tuple[list[int], list[int]]:
        return None
    
    def get_cross_points(self, cities_nb) -> tuple[int, int]:
        # crossover_lt = (int) (self.crossover_size_rate * cities_nb)
        segment_length = self.get_segment_length(cities_nb)
        idx_a = randint(0, cities_nb - segment_length)
        idx_b = idx_a + segment_length
        return (idx_a, idx_b)
