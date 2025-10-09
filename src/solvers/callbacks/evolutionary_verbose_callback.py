from solvers.callbacks.evolutionary_callback import EvolutionaryCallback
from stop_criterions.stop_criterion import StopCriterion

from math import inf
import time
import json

class EvolutionaryVerboseLevel1Callback(EvolutionaryCallback):
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.iteration_count = 0
        self.convergence_data = []
        self.best_cost_history = []
        
    def on_start(self, coordinates: list[tuple[float, float]], generation: list[list[int]]):
        self.start_time = time.time()
        self.iteration_count = 0
        self.convergence_data = []
        self.best_cost_history = []
        print(f"SOLVER_START: Starting evolutionary algorithm with {len(coordinates)} cities, population size {len(generation)}")
    
    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        self.iteration_count += 1
        current_best = elites[0][1]
        self.best_cost_history.append(current_best)

        self.convergence_data.append({
            'iteration': self.iteration_count,
            'best_cost': current_best,
            'time_elapsed': time.time() - self.start_time if self.start_time else 0
        })
    
    def on_stop(self, result: bool, and_criterions: list[StopCriterion], and_criterions_results: list[bool], or_criterions: list[StopCriterion], or_criterions_results: list[bool]):
        if not result:
            return
        and_stoppages = []
        for i in range(len(and_criterions_results)):
            if and_criterions_results[i]:
                    and_stoppages.append(str(and_criterions[i]))
        log_str = "STOPPAGE_CRITERIA:"
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
    
    def on_end(self, order: list[int], cost: float):
        execution_time = time.time() - self.start_time if self.start_time else 0
        
        print(f"FINAL_RESULT_START")
        print(f"BEST_COST: {cost}")
        print(f"EXECUTION_TIME: {execution_time:.6f}")
        print(f"TOTAL_ITERATIONS: {self.iteration_count}")
        print(f"CONVERGENCE_DATA: {json.dumps(self.convergence_data)}")
        print(f"FINAL_RESULT_END")


class EvolutionaryVerboseLevel2Callback(EvolutionaryVerboseLevel1Callback):
    def __init__(self) -> None:
        super().__init__()
        self.best_cost = inf
    
    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        super().on_new_elites(elites)
        
        current_best = elites[0][1]
        if self.best_cost > current_best:
            self.best_cost = current_best
            improvement = ((self.best_cost_history[-2] - current_best) / self.best_cost_history[-2] * 100) if len(self.best_cost_history) > 1 else 0
            print(f"ITERATION_{self.iteration_count}: New best cost: {current_best:.4f} (improvement: {improvement:.2f}%)")

class EvolutionaryVerboseLevel3Callback(EvolutionaryVerboseLevel2Callback):
    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        super().on_new_elites(elites)

        top_elites = elites[:min(3, len(elites))]
        elite_costs = [f"{elite[1]:.4f}" for elite in top_elites]
        print(f"ITERATION_{self.iteration_count}_ELITES: Top {len(top_elites)} costs: {', '.join(elite_costs)}")
