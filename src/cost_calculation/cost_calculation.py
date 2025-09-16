class CostCalculation():
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        raise NotImplementedError
    
class EuclideanCostCalculation(CostCalculation):
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        return ((pt1[1] - pt1[0])**2 + (pt2[1] - pt2[0])**2)**0.5
    
class ManhattanCostCalculation(CostCalculation):
    def calculate(self, pt1: tuple[float, float], pt2: tuple[float, float]) -> float:
        return abs(pt1[1] - pt1[0]) + abs(pt2[1] - pt2[0])