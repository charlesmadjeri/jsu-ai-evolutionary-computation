from solvers.callbacks.evolutionary_callback import EvolutionaryCallback
from stop_criterions.stop_criterion import StopCriterion

from math import inf

class EvolutionaryVerboseLevel1Callback(EvolutionaryCallback):
    def on_stop(self, result: bool, and_criterions: list[StopCriterion], and_criterions_results: list[bool], or_criterions: list[StopCriterion], or_criterions_results: list[bool]):
        if not result:
            return
        and_stoppages = []
        for i in range(len(and_criterions_results)):
            if and_criterions_results[i]:
                    and_stoppages.append(str(and_criterions[i]))
        log_str = "Stoppage criterions met:"
        if len(and_stoppages) > 0:
            log_str += f" and[{', '.join(and_stoppages)}]"
        if len(or_criterions) > 0:
            or_stoppages = []
            for i in range(len(or_criterions_results)):
                if or_criterions_results[i]:
                    or_stoppages.append(str(or_criterions[i]))
            if len(or_stoppages) > 0:
                log_str += f" or[{', '.join(or_stoppages)}]"
        print(log_str)


class EvolutionaryVerboseLevel2Callback(EvolutionaryCallback):
    def __init__(self) -> None:
        super().__init__()
        self.best_cost = inf
        self.iteration = 0
    
    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        self.iteration += 1
        if self.best_cost > elites[0][1]:
            self.best_cost = elites[0][1]
            print(f"{self.iteration}: New best cost: {elites[0][1]} for order {elites[0][0]}")

class EvolutionaryVerboseLevel3Callback(EvolutionaryCallback):
    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        print(f"New elites: {elites}")
