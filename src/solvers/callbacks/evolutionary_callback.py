from abc import ABC

class EvolutionaryCallback(ABC):
    def on_start(self, dataset: list[tuple[float, float]], starting_generation: list[list[int]]):
        pass

    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        pass

    def on_new_generation(self, generation: list[list[int]]):
        pass

    def on_end(self, order: list[int], cost: float):
        pass