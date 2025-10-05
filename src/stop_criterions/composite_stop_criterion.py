from .stop_criterion import StopCriterion

class AndStopCriterion(StopCriterion):
    def __init__(self, criteria: list[StopCriterion]):
        if not criteria:
            raise ValueError("criteria list cannot be empty")
        self.criteria = criteria

    def restart(self):
        for criterion in self.criteria:
            criterion.restart()

    def check_continue(self, best_distance: float) -> bool:
        return all(c.check(best_distance) for c in self.criteria)

    def check(self, value): 
        return self.check_continue(value)

    def start(self):        
        for c in self.criteria:
            c.start()

    def end(self):           
        for c in self.criteria:
            c.end()

    def __str__(self):
        return "AND(" + ",".join(str(c) for c in self.criteria) + ")"


class OrStopCriterion(StopCriterion):
    def __init__(self, criteria: list[StopCriterion]):
        if not criteria:
            raise ValueError("criteria list cannot be empty")
        self.criteria = criteria

    def restart(self):
        for criterion in self.criteria:
            criterion.restart()

    def check_continue(self, best_distance: float) -> bool:
        return any(c.check(best_distance) for c in self.criteria)

    def check(self, value):  
        return self.check_continue(value)

    def start(self):        
        for c in self.criteria:
            c.start()

    def end(self):         
        for c in self.criteria:
            c.end()

    def __str__(self):
        return "OR(" + ",".join(str(c) for c in self.criteria) + ")"
