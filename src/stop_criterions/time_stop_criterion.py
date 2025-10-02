import time
from src.stop_criterions.stop_criterion import StopCriterion

class TimeStopCriterion(StopCriterion):
    def __init__(self, total_seconds: int):
        assert total_seconds > 0
        self.total_seconds = total_seconds
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def check(self, total_distance: float):
        return (time.time() - self.start_time) <= self.total_seconds

    def end(self):
        self.start_time = None