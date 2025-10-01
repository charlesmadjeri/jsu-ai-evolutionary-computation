from solvers.solver import Solver
from cost_calculation.cost_calculation import CostCalculation

"""
Greedy first algorithm solver implementation.
"""
class GreedyFirst(Solver):
    """
    Args:
        cost_calculator: CostCalculation - extended CostCalculation class that will be used to calculate the cost between two points.
        round_trip: bool - whether to include the cost from the last point to the first point in the total distance.
        minimise_cost: bool - whether to minimise the cost or maximise the cost.
    """
    def __init__(self, cost_calculator: CostCalculation, round_trip=False, minimise_cost=True):
        super().__init__()
        self.cost_calculator = cost_calculator
        self.round_trip = round_trip
        self.check_is_better_cost = lambda x, y: x < y if minimise_cost else x > y

    def solve(self,coordinates:list[tuple[float,float]]) -> tuple [list[int],float]:
        if not coordinates:
            raise ValueError("coordinates list can not be empty")
        if len(coordinates) == 1:
            return [0], 0
        
        remaining = list(range(len(coordinates)))
        visited = [remaining.pop(0)]
        total_distance = 0

        self.metric_tracker.log("start_node", visited[0])

        while remaining:
            self.metric_tracker.log("greedy_step", 1)

            last = visited[-1]
            best_i = 0
            best_d = self.cost_calculator.calculate(coordinates[last],coordinates[remaining[0]])
            self.metric_tracker.log("distance_calculation", 1)

            for i in range(1,len(remaining)):
                d = self.cost_calculator.calculate(coordinates[last],coordinates[remaining[i]])
                self.metric_tracker.log("distance_calculations", 1)
                if self.check_is_better_cost(d,best_d):
                    best_i = i
                    best_d = d

            total_distance += best_d
            visited.append(remaining.pop(best_i))

        if self.round_trip:
            d = self.cost_calculator.calculate(
                coordinates[visited[-1]],
                coordinates[visited[0]]
            )
            total_distance += d
            self.metric_tracker.log("distance_calculations", 1)

        self.metric_tracker.log("final_distance", total_distance)
        self.metric_tracker.log("nodes_visited", len(visited))

        return visited, total_distance
