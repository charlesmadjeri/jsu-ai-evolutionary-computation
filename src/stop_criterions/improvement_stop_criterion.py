from stop_criterions.stop_criterion import StopCriterion

class ImprovementStopCriterion(StopCriterion):
    def __init__(self, min_improvement: float, maximise: bool = False):
        assert min_improvement > 0.
        self.min_improvement = min_improvement
        self.maximise = maximise
        if self.maximise:
            self.calculate_improvement = lambda current_cost, old_cost: (current_cost / old_cost) - 1.
        else:
            self.calculate_improvement = lambda current_cost, old_cost: (old_cost / current_cost) - 1.
        self.restart()

    def restart(self):
        self.previous_distance = None
        self.improvement = 0.

    def check_continue(self, total_distance: float) -> bool:
        if self.previous_distance is None:
            self.previous_distance = total_distance
            return True
        self.improvement = self.calculate_improvement(total_distance, self.previous_distance)
        self.previous_distance = total_distance
        return self.improvement >= self.min_improvement

    def __str__(self) -> str:
        return f"ImprovementStopCriterion(min_improvement={self.min_improvement}, latest_improvement={self.improvement})"