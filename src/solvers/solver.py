from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve(self, coordinates: list[tuple[float, float]]):
        raise NotImplementedError
        return sorted(coordinates)

    @abstractmethod
    def mutate(self):
        if (False): # put placeholder condition in order to always return false, will be replaced with mutation status
            return True 
        return False