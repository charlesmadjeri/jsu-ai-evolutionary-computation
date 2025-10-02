from src.stop_criterions.stop_criterion import StopCriterion

class IterationsStopCriterion(StopCriterion):
    def __init__(self, total_iterations: int):
        assert total_iterations > 0
        self.current_iteration = 0
        self.total_iterations = total_iterations

    def start(self):
        self.current_iteration = 0

    def check(self, total_distance: float):
        self.current_iteration += 1
        return self.current_iteration <= self.total_iterations

    def end(self):
        self.current_iteration = 0