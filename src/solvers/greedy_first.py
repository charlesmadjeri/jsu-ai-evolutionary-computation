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

    def solve(self, coordinates: list[tuple[float, float]])  -> tuple[list[tuple[float, float]], float]:
        if len(coordinates) == 0:
            raise ValueError("Coordinates list can't be empty")
        if len(coordinates) == 1:
            return coordinates, 0

        remaining = coordinates.copy()
        visited = []
        visited.append(remaining.pop(0))
        total_distance = 0
        while True:
            candidate_index = 0
            candidate_distance = self.cost_calculator.calculate(visited[-1], remaining[0])
            for i in range(1, len(remaining)):
                distance = self.cost_calculator.calculate(visited[-1], remaining[i])
                if self.check_is_better_cost(distance, candidate_distance):
                    candidate_index = i
                    candidate_distance = distance
            total_distance += candidate_distance
            visited.append(remaining.pop(candidate_index))
            if len(remaining) == 1:
                total_distance += self.cost_calculator.calculate(visited[-1], remaining[0])
                visited.append(remaining.pop(0))
                if self.round_trip:
                    total_distance += self.cost_calculator.calculate(visited[-1], visited[0])
                break
        return visited, total_distance
