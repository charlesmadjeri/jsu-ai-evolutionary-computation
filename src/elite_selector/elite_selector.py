from src.cost_calculation.cost_calculation import CostCalculation

class EliteSelector():
    def __init__(self, coordinates: list[tuple[float, float]], cost_calculator: CostCalculation, elite_size: int):
        self.coordinates = coordinates
        self.cost_calculator = cost_calculator
        self.elite_size = elite_size

    def calculate_cost(self, generation) -> list[float]:
        cost = []
        for i in range(len(generation)):
            cost.append(0)
            for j in range(1, len(generation[i])):
                cost[i] += self.cost_calculator.calculate(self, self.coordinates[generation[i][j-1] - 1], self.coordinates[generation[i][j] - 1])
        return cost
    
    def find_elite_elements(self, generation) -> list[list[int]]:
        elites = []
        cost = self.calculate_cost(generation)
        for i in sorted(cost)[:self.elite_size]:
            elites.append(generation[cost.index(i)])
        return elites