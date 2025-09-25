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
        self.cost_calculator = cost_calculator
        self.round_trip = round_trip
        self.check_is_better_cost = lambda x, y: x < y if minimise_cost else x > y

    def solve(self,coordinates:list[tuple[float,float]]) -> tuple [list[int],float]:
        if len(coordinates) == 0:
            raise ValueError("coordinates list can not be empty")
        if len(coordinates) == 1:
            return [0], 0
        
        remaining = list(range(len(coordinates)))
        visited = [remaining.pop(0)]
        
        total_distance = 0
        while True:
            last = visited[-1]
            best_i = 0
            best_d = self.cost_calculator.calculate(
                coordinates[last],
                coordinates[remaining[0]]
            )

            for i in range(1,len(remaining)):
                d = self.cost_calculator.calculate(
                    coordinates[last],
                    coordinates[remaining[i]]
                )
                if self.check_is_better_cost(d,best_d):
                    best_i = i
                    best_d = d

                    total_distance += best_d
                    visited.append(remaining.pop(best_i))

                    if len(remaining) == 1:
                        total_distance += self.cost_calculator.calculate(
                            coordinates[visited[-1]],
                            coordinates[remaining[0]]
                        )
            break

        return visited, total_distance
    