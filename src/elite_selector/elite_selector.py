from src.cost_calculation.cost_calculation import CostCalculation

class EliteSelector():
    def __init__(self, generation: list[list[int]], coordinates: list[tuple[float, float]], cost_calculator: CostCalculation, elite_size: int):
        self.generation = generation
        self.coordinates = coordinates
        self.cost = []
        self.elites = []
        self.cost_calculator = cost_calculator
        self.elite_size = elite_size

    def calculate_cost(self) -> list[float]:
        for i in range(len(self.generation)):
            self.cost.append(0)
            for j in range(1, len(self.generation[i])):
                self.cost[i] += self.cost_calculator.calculate(self, self.coordinates[self.generation[i][j-1] - 1], self.coordinates[self.generation[i][j] - 1])
        return self.cost
    
    def find_elite_elements(self) -> list[list[int]]:
        self.cost = []
        self.elites = []
        self.cost = self.calculate_cost()
        for i in sorted(self.cost)[:self.elite_size]:
            self.elites.append(self.generation[self.cost.index(i)])
        return self.elites