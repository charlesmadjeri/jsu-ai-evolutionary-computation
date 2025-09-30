from abc import ABC, abstractmethod

class EliteSelector(ABC):
    @abstractmethod
    def __init__(self, generation = list[list[int]], coordinates = list[tuple[float, float]]):
        self.generation = generation
        self.coordinates = coordinates
        self.cost = []
        self.elites = []

    @abstractmethod
    def calculate_cost(self) -> list[float]:
        return None
    
    @abstractmethod
    def find_elite_elements(self, elite_size = float) -> list[list[int]]:
        self.cost = self.calculate_cost()
        for i in sorted(self.cost)[:elite_size]:
            self.elites.append(self.generation[self.cost.index(i)])
        return self.elites