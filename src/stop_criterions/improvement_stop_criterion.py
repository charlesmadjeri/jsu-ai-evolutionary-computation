from src.stop_criterions.stop_criterion import StopCriterion

class ImprovementStopCriterion(StopCriterion):
    def __init__(self, min_improvement: float):
        assert min_improvement > 0.
        self.min_improvement = min_improvement
        self.previous_distance = None

    def start(self):
        self.previous_distance = None

    def check(self, total_distance: float):
        if self.previous_distance is None:
            self.previous_distance = total_distance
            return True
        improvement = (total_distance / self.previous_distance) - 1.
        self.previous_distance = total_distance
        return improvement >= self.min_improvement

    def end(self):
        self.previous_distance = None