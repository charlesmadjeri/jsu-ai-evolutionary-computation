from solvers.callbacks.greedy_first_callback import GreedyFirstCallback
from solvers.solver import Solver
from cost_calculation.cost_calculation import CostCalculation
"""
Greedy first algorithm solver implementation.
"""
class GreedyFirst(Solver):
    """
    Args:
        cost_calculator: CostCalculation - extended CostCalculation class that will be used to calculate the cost between two points.
        minimise_cost: bool - whether to minimise the cost or maximise the cost.
    """
    def __init__(self, cost_calculator: CostCalculation, minimise_cost=True, callbacks: list[GreedyFirstCallback] = []):
        self.cost_calculator = cost_calculator
        self.check_is_better_cost = lambda x, y: x < y if minimise_cost else x > y
        self.callbacks = callbacks
        
    def solve(self, coordinates: list[tuple[float, float]]) -> tuple[list[int], float]:
        if not coordinates:
            raise ValueError("coordinates list can not be empty")
        if len(coordinates) == 1:
            return [0], 0
        
        remaining = list(range(len(coordinates)))
        visited = [remaining.pop(0)]
        
        for callable in self.callbacks:
            callable.on_start(dataset=coordinates, starting_node=visited[0])
        
        iteration_i = 0
        while remaining:
            iteration_i += 1
            for callable in self.callbacks:
                callable.on_iteration(processing_node=iteration_i)
            last = visited[-1]
            best_i = 0
            best_d = self.cost_calculator.calculate(
                coordinates[last],
                coordinates[remaining[0]]
            )
            for callable in self.callbacks:
                callable.on_cost_calculation(last, remaining[0], best_d)
            
            for i in range(1, len(remaining)):
                d = self.cost_calculator.calculate(
                    coordinates[last],
                    coordinates[remaining[i]]
                )
                for callable in self.callbacks:
                    callable.on_cost_calculation(last, remaining[i], d)
                
                if self.check_is_better_cost(d, best_d):
                    best_i = i
                    best_d = d
            
            visited.append(remaining.pop(best_i))
        
        total_distance = sum(
            self.cost_calculator.calculate(
                coordinates[visited[i]], 
                coordinates[visited[i + 1]]
            )
            for i in range(len(visited) - 1)
        )
        
        for callable in self.callbacks:
            callable.on_end(order=visited, cost=total_distance)
        return visited, total_distance