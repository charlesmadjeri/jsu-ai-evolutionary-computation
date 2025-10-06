from abc import ABC

from stop_criterions.stop_criterion import StopCriterion

class EvolutionaryCallback(ABC):
    def on_start(self, dataset: list[tuple[float, float]], starting_generation: list[list[int]]):
        pass

    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        pass

    def on_new_generation(self, generation: list[list[int]]):
        pass

    def on_stop(self, result: bool, and_critertions: list[StopCriterion], and_criterions_results: list[bool], or_critertions: list[StopCriterion], or_criterions_results: list[bool]):
        pass

    def on_end(self, order: list[int], cost: float):
        pass