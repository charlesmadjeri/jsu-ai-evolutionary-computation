from cost_calculation import CostCalculation

class ManhattanCostCalculation(CostCalculation):
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        return abs(pt2[0] - pt1[0]) + abs(pt2[1] - pt1[1])