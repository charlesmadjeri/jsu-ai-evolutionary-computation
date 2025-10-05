from stop_criterions.stop_criterion import StopCriterion

class AndStopCriterion(StopCriterion):
    def __init__(self, criteria:StopCriterion):
        self.criteria = criteria 

    def restart(self):
        for criterion in self.criteria:
            criterion.restart()

    def check_continue(self, best_distance:float) -> bool:
        return all(criterion.check_continue(best_distance) for criterion in self.criteria)
    
    def __str__(self):
        return " AND ("+",".join(str(c) for c in self.criteria)+")"

class OrStopCriterion(StopCriterion):
    def __init__(self, criteria:StopCriterion):
        self.criteria = criteria

    def restart(self):
        for c in self.criteria:
            c.restart()

    def check_continue(self, best_distance:float) -> bool:
        return any(c.check(best_distance) for c in self.criteria)
    
    def __str__(self):
        return " OR ("+",".join(str(c) for c in self.criteria)+")"