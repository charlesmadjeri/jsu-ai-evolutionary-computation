from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from crossover.order_crossover import OrderCrossover
from elite_selector.elite_selector import EliteSelector
from solvers.callbacks.evolutionary_callback import EvolutionaryCallback
from solvers.evolutionary_solver import EvolutionarySolver

class TestEvolutionaryCallback(EvolutionaryCallback):
    def __init__(self):
        self.start_c = 0
        self.new_elites_c = 0
        self.new_generation_c = 0
        self.end_c = 0

    def on_start(self, dataset: list[tuple[float, float]], starting_generation: list[list[int]]):
        self.start_c += 1

    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        self.new_elites_c += 1

    def on_new_generation(self, generation: list[list[int]]):
        self.new_generation_c += 1

    def on_end(self, order: list[int], cost: float):
        self.end_c += 1

def test_evolutionary_callback():
    callback_1 = TestEvolutionaryCallback()
    callback_2 = TestEvolutionaryCallback()
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, 2),
        crossover=OrderCrossover(3),
        stop_criterions=[],
        population_size=3,
        verbose_level=0,
        minimum_iterations=10,
        callbacks=[callback_1, callback_2]
    )
    dataset = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    solver.solve(dataset)
    assert callback_1.start_c == callback_2.start_c == 1
    assert callback_1.new_elites_c == callback_2.new_elites_c == 11
    assert callback_1.new_generation_c == callback_2.new_generation_c == 10
    assert callback_1.end_c == callback_2.end_c == 1