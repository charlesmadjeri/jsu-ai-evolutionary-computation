import time
from stop_criterions.stop_criterion import StopCriterion

class TimeStopCriterion(StopCriterion):
    def __init__(self, total_seconds: int):
        assert total_seconds > 0
        self.total_seconds = total_seconds

    def start(self):
        self.start_time = time.time()
        self.elapsed_time = 0

    def check(self, total_distance: float):
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time <= self.total_seconds

    def __str__(self):
        return f"TimeStopCriterion(total_seconds={self.total_seconds}, elapsed_time={self.elapsed_time})"