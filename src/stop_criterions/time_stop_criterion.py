import time
from stop_criterions.stop_criterion import StopCriterion

class TimeStopCriterion(StopCriterion):
    def __init__(self, total_seconds: float):
        assert total_seconds > 0
        self.total_seconds = total_seconds
        self.restart()

    def restart(self):
        self.start_time = time.time()
        self.elapsed_time = 0

    def check_continue(self, total_distance: float) -> bool:
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time <= self.total_seconds

    def __str__(self) -> str:
        return f"TimeStopCriterion(total_seconds={self.total_seconds}, elapsed_time={self.elapsed_time})"