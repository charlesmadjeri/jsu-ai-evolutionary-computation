from itertools import chain
from random import sample
from solvers.callbacks.evolutionary_callback import EvolutionaryCallback
from solvers.solver import Solver

from elite_selector.elite_selector import EliteSelector
from stop_criterions.iterations_stop_criterion import IterationsStopCriterion
from stop_criterions.stop_criterion import StopCriterion
from crossover.crossover import Crossover


class EvolutionarySolver(Solver):
    def __init__(self, 
            elite_selector: EliteSelector, 
            crossover: Crossover, 
            stop_criterions: list[StopCriterion],
            population_size: int,
            verbose_level: int = 0,
            # maximise: bool = False, # TODO implement
            callbacks: list[EvolutionaryCallback] = [],
            minimum_iterations: int = 25):
        
        if population_size < 3 or population_size <= elite_selector.elite_size:
            raise ValueError(f"Population size must be greater than 3 and greater than elite size, but got population_size={population_size} and elite_size={elite_selector.elite_size}")
        
        self.elite_selector = elite_selector
        self.crossover = crossover
        self.callbacks = callbacks
        self.or_criterions = stop_criterions if isinstance(stop_criterions, list) else []
        self.and_criterions = [IterationsStopCriterion(minimum_iterations)]
        self.verbose_level = verbose_level
        self.has_or_criterions = len(self.or_criterions) > 0
        self.population_size = population_size
        
        # this lambda is needed so if there is none 'or criterion' it will always return True
        if self.has_or_criterions:
            self.get_or_criterions_stop_result = lambda x: [not criterion.check_continue(x) for criterion in self.or_criterions]
        else:
            self.get_or_criterions_stop_result = lambda x: [True]

    def check_should_stop(self, best_distance: float) -> bool:
        and_stop_results = [not criterion.check_continue(best_distance) for criterion in self.and_criterions]
        or_stop_results = self.get_or_criterions_stop_result(best_distance)
        should_stop = all(and_stop_results) and any(or_stop_results)
        if should_stop and self.verbose_level > 0:
            and_stoppages = []
            for i in range(len(and_stop_results)):
                if and_stop_results[i]:
                        and_stoppages.append(str(self.and_criterions[i]))
            log_str = "Stoppage criterions met:"
            if len(and_stoppages) > 0:
                log_str += f" and[{', '.join(and_stoppages)}]"
            if self.has_or_criterions:
                or_stoppages = []
                for i in range(len(or_stop_results)):
                    if or_stop_results[i]:
                        or_stoppages.append(str(self.or_criterions[i]))
                if len(or_stoppages) > 0:
                    log_str += f" or[{', '.join(or_stoppages)}]"
            print(log_str)
        return should_stop

    def create_new_generation(self, elites: list[tuple[list[int], float]]) -> list[list[int]]:
        generation = [elite_pair[0] for elite_pair in elites]
        while len(generation) < self.population_size:
            elite_pair = sample(elites, 2)
            child_a, child_b = self.crossover.crossover((elite_pair[0][0], elite_pair[1][0]))
            generation.append(child_a)
            generation.append(child_b)
        if len(generation) > self.population_size:
            generation.pop()
        return generation
        
    def solve(self, coordinates: list[tuple[float, float]]) -> tuple[list[int], float]:
        solution_size = len(coordinates)
        if self.crossover.segment_length is not None and solution_size <= self.crossover.segment_length:
            raise ValueError(f"Solution size must be greater than crossover segment length, but got solution_size={solution_size} and crossover_segment_length={self.crossover.segment_length}")

        for criterion in chain(self.or_criterions, self.and_criterions):
            criterion.restart()
        generation = [sample(range(solution_size), solution_size) for _ in range(self.population_size)]

        for callback in self.callbacks:
            callback.on_start(coordinates, generation)

        while True:
            elites = self.elite_selector.find_elite_elements(coordinates, generation)

            elites.sort(key=lambda x: x[1])
            best_distance = elites[0][1]

            for callback in self.callbacks:
                callback.on_new_elites(elites)
            
            if self.check_should_stop(best_distance):
                break
            
            generation = self.create_new_generation(elites)            

            for callback in self.callbacks:
                callback.on_new_generation(generation)

        for callback in self.callbacks:
            callback.on_end(order=elites[0][0], cost=elites[0][1])
        return elites[0]