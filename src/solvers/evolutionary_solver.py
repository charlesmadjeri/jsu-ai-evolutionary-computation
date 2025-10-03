from itertools import chain
from random import sample
from crossover import crossover
from elite_selector import elite_selector
from solvers.solver import Solver

from elite_selector.elite_selector import EliteSelector
from stop_criterions.iterations_stop_criterion import IterationsStopCriterion
from stop_criterions.stop_criterion import StopCriterion
from crossover.crossover import Crossover

MINIMUM_ITERATIONS = 25

class EvolutionarySolver(Solver):
    def __init__(self, elite_selector: EliteSelector, crossover: Crossover, stop_criterions: list[StopCriterion], verbose_level: int = 0):
        self.elite_selector = elite_selector
        self.crossover = crossover
        # TODO once 'and' and 'or' logical operators are implemented, use them instead of lists
        self.or_criterions = stop_criterions
        self.and_criterions = [IterationsStopCriterion(MINIMUM_ITERATIONS)]
        self.verbose_level = verbose_level

        # this lambda is needed so if there is none 'or criterion' it will always return True
        if len(self.or_criterions) > 0:
            self.get_or_criterions_result = lambda x: [criterion.check(x) for criterion in self.or_criterions]
        else:
            self.get_or_criterions_result = lambda x: [True]
        
    def solve(self, coordinates: list[tuple[float, float]]) -> tuple[list[int], float]:
        solution_size = len(coordinates)
        population_size = self.elite_selector.population_size
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
            and_stoppage_results = [criterion.check(best_distance) for criterion in self.or_criterions]
            or_stoppage_results = self.get_or_criterions_result(best_distance)
            if all(and_stoppage_results) and any(or_stoppage_results):
                # print stoppage criterions that met
                if self.verbose_level > 0:
                    and_positive_stoppages = []
                    or_positive_stoppages = []
                    for i in range(len(and_stoppage_results)):
                        if and_stoppage_results[i]:
                            and_positive_stoppages.append(self.and_criterions[i])
                    for i in range(len(or_stoppage_results)):
                        if or_stoppage_results[i]:
                            or_positive_stoppages.append(self.or_criterions[i])
                    log_str = "Stoppage criterions met:"
                    if len(and_positive_stoppages) > 0:
                        log_str += f" and[{and_positive_stoppages.join(', ')}]"
                    if len(or_positive_stoppages) > 0:
                        log_str += f" or {or_positive_stoppages}"
                    print(log_str)
                break
            generation = [elite_pair[0] for elite_pair in elites]
            while len(generation) < population_size:
                # pick random elite pair
                elite_pair = sample(elites, 2)
                # crossover
                child_a, child_b = self.crossover.crossover(elite_pair)
                # add to generation
                generation.append(child_a)
                generation.append(child_b)
            if len(generation) > population_size:
                generation.pop()    
        return elites[0]