from cost_calculation.cost_calculation import CostCalculation

class EuclideanCostCalculation(CostCalculation):
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        return ((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)**0.5