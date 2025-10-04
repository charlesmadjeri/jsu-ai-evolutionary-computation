from itertools import chain
from random import sample
from crossover import crossover
from elite_selector import elite_selector
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
            minimum_iterations: int = 25):
        if not (population_size >= 3 and population_size > elite_selector.elite_size):
            raise ValueError(f"Population size must be greater than 3 and greater than elite size, but got population_size={population_size} and elite_size={elite_selector.elite_size}")
        
        self.elite_selector = elite_selector
        self.crossover = crossover
        # TODO once 'and' and 'or' logical operators are implemented, use them instead of lists
        self.or_criterions = stop_criterions
        self.and_criterions = [IterationsStopCriterion(minimum_iterations)]
        self.verbose_level = verbose_level
        self.has_or_criterions = len(self.or_criterions) > 0
        self.population_size = population_size
        
        # this lambda is needed so if there is none 'or criterion' it will always return True
        if self.has_or_criterions:
            self.get_or_criterions_result = lambda x: [criterion.check(x) for criterion in self.or_criterions]
        else:
            self.get_or_criterions_result = lambda x: [True]

    def check_should_stop(self, best_distance: float) -> bool:
        and_stoppage_results = [criterion.check(best_distance) for criterion in self.or_criterions]
        or_stoppage_results = self.get_or_criterions_result(best_distance)
        should_stop = all(and_stoppage_results) and any(or_stoppage_results)
        if should_stop and self.verbose_level > 0:
            and_positive_stoppages = []
            for i in range(len(and_stoppage_results)):
                if and_stoppage_results[i]:
                    and_positive_stoppages.append(self.and_criterions[i])
            log_str = "Stoppage criterions met:"
            if len(and_positive_stoppages) > 0:
                log_str += f" and[{and_positive_stoppages.join(', ')}]"
            if self.has_or_criterions:
                or_positive_stoppages = []
                for i in range(len(or_stoppage_results)):
                    if or_stoppage_results[i]:
                        or_positive_stoppages.append(self.or_criterions[i])
                if len(or_positive_stoppages) > 0:
                    log_str += f" or[{or_positive_stoppages.join(', ')}]"
            print(log_str)
        return should_stop

    def create_new_generation(self, elites: list[tuple[list[int], float]]) -> list[list[int]]:
        generation = [elite_pair[0] for elite_pair in elites]
        while len(generation) < self.elite_selector.population_size:
            elite_pair = sample(elites, 2)
            child_a, child_b = self.crossover.crossover(elite_pair)
            generation.append(child_a)
            generation.append(child_b)
        if len(generation) > self.elite_selector.population_size:
            generation.pop()
        return generation
        
    def solve(self, coordinates: list[tuple[float, float]]) -> tuple[list[int], float]:
        solution_size = len(coordinates)
        for criterion in chain(self.or_criterions, self.and_criterions):
            criterion.start()
        generation = [sample(range(solution_size), solution_size) for _ in range(population_size)]
        
        while True:
            # TODO update find_elite_elements to contain also total distance -> list[tuple(list[int], float)]
            elites = self.elite_selector.find_elite_elements(generation)

            # check stoppage criterions
            # TODO: verify that this is correct && if we use maximisation it should be reversed
            elites.sort(key=lambda x: x[1])
            best_distance = elites[0][1]
            # TODO REMOVEME
            assert best_distance <= elites[1][1]
            
            if self.check_should_stop(best_distance):
                break
            
            generation = self.create_new_generation(elites)            
        return elites[0]