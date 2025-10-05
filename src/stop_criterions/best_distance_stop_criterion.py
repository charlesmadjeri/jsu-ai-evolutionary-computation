from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from dataparser.main import load_tsp_data
from solvers.greedy_first import GreedyFirst
from stop_criterions.stop_criterion import StopCriterion

class BestDistanceStopCriterion(StopCriterion):
    def __init__(self, algorithm_name):
        solver = GreedyFirst(ManhattanCostCalculation, minimise_cost=True)
        data = load_tsp_data(f"data/TSPLIB/{algorithm_name}.tsp")
        data = [(float(x), float(y)) for x, y in data]
        _, self.threshold_distance = solver.solve(data)
        self.restart()

    def restart(self):
        pass
    
    def check_continue(self, total_distance: float) -> bool:
        return total_distance <= self.threshold_distance
    
    def __str__(self) -> str:
        return f"BestDistanceStopCriterion(threshold_distance={self.threshold_distance})"