from cost_calculation.cost_calculation import CostCalculation

class EliteSelector():
    def __init__(self, cost_calculator: CostCalculation, elite_size: int):
        if elite_size < 2:
            raise ValueError(f"Elite size must be greater than 2, but got elite_size={elite_size}")
        
        self.cost_calculator = cost_calculator
        self.elite_size = elite_size

    def calculate_cost(self, coordinates: list[tuple[float, float]], generation) -> list[float]:
        cost = []
        for i in range(len(generation)):
            cost.append(0)
            for j in range(1, len(generation[i])):
                cost[i] += self.cost_calculator.calculate(coordinates[generation[i][j-1]], coordinates[generation[i][j]])
        return cost
    
    def find_elite_elements(self, coordinates: list[tuple[float, float]], generation) -> list[tuple[list[int], float]]:
        elites = []
        original_costs = self.calculate_cost(coordinates, generation)
        top_costs = sorted(enumerate(original_costs), key=lambda x: x[1])[:self.elite_size]
        for idx, cost_value in top_costs:
            elites.append((generation[idx], cost_value))
        return elites