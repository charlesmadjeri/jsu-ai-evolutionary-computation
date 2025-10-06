from stop_criterions.stop_criterion import StopCriterion

class ThresholdCostStopCriterion(StopCriterion):
    def __init__(self, threshold_distance: float):
        self.threshold_distance = threshold_distance
        self.restart()

    def restart(self):
        self.total_distance = 0.0
    
    def check_continue(self, total_distance: float) -> bool:
        self.total_distance = total_distance
        return self.total_distance <= self.threshold_distance
    
    def __str__(self) -> str:
        return f"ThresholdCostStopCriterion(threshold_distance={self.threshold_distance}, total_distance={self.total_distance})"