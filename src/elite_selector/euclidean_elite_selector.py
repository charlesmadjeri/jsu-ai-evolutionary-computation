from elite_selector.elite_selector import EliteSelector
from cost_calculation.euclidean_cost_calculation import EuclideanCostCalculation

class EuclideanEliteSelector(EliteSelector):
    def __init__(self, generation = list[list[int]], coordinates = list[tuple[float, float]]):
        super().__init__(generation, coordinates)
        
    def calculate_cost(self) -> list[float]:
        for i in range(len(self.generation)):
            self.cost.append(0)
            for j in range(1, len(self.generation[i])):
                self.cost[i] += EuclideanCostCalculation.calculate(self, self.coordinates[self.generation[i][j-1] - 1], self.coordinates[self.generation[i][j] - 1])
        return self.cost
    
    def find_elite_elements(self, elite_size = float) -> list[list[int]]:
        return super().find_elite_elements(elite_size)