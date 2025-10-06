from abc import ABC

class GreedyFirstCallback(ABC):
    def on_start(self, dataset: list[tuple[float, float]], starting_node: int):
        pass

    def on_iteration(self, processing_node: int):
        pass

    def on_cost_calculation(self, node_a: int, node_b: int, result: float):
        pass

    def on_end(self, order: list[int], cost: float):
        pass