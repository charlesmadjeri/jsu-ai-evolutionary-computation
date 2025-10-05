from stop_criterions.stop_criterion import StopCriterion

class IterationsStopCriterion(StopCriterion):
    def __init__(self, total_iterations: int):
        assert total_iterations > 0
        self.total_iterations = total_iterations
        self.restart()

    def restart(self):
        self.current_iteration = 0

    def check_continue(self, total_distance: float) -> bool:
        self.current_iteration += 1
        return self.current_iteration <= self.total_iterations

    def __str__(self) -> str:
        return f"IterationsStopCriterion(current={self.current_iteration}, total={self.total_iterations})"