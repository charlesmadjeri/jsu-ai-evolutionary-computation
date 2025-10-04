from src.cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from src.elite_selector.elite_selector import EliteSelector
from src.solvers.evolutionary_solver import EvolutionarySolver
from src.stop_criterions.iterations_stop_criterion import IterationsStopCriterion
from src.crossover.order_crossover import OrderCrossover
from stop_criterions.improvement_stop_criterion import ImprovementStopCriterion
from stop_criterions.time_stop_criterion import TimeStopCriterion

from time import sleep
from pytest import raises

TEST_COORDINATES = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]

def test_init_small_population_size():
    for population_size in range(3):
        with raises(ValueError):
            solver = EvolutionarySolver(
                elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
                crossover=OrderCrossover(0.3),
                stop_criterions=[],
                population_size=population_size,
                verbose_level=10,
                minimum_iterations=10
            )

def test_init_population_less_than_elite_size():
    with raises(ValueError):
        solver = EvolutionarySolver(
            elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=100),
            crossover=OrderCrossover(0.3),
            stop_criterions=[],
            population_size=99,
            verbose_level=10,
            minimum_iterations=10
        )

def test_none_stoppage_criterions():
    minimum_iterations = 10
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[],
        population_size=100,
        verbose_level=10,
        minimum_iterations=minimum_iterations
    )

    for i in range(minimum_iterations):
        assert solver.check_should_stop(i) == False
    assert solver.check_should_stop(123) == True

def test_one_iteration_stoppage_criterion():
    minimum_iterations = 10
    it_crit = IterationsStopCriterion(minimum_iterations * 2)
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[it_crit],
        population_size=100,
        verbose_level=10,
        minimum_iterations=minimum_iterations
    )

    for i in range(it_crit.total_iterations):
        assert solver.check_should_stop(i) == False
    assert solver.check_should_stop(123) == True

def test_one_time_stoppage_criterion():
    time_crit = TimeStopCriterion(.2)
    min_it = 10
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[time_crit],
        population_size=100,
        verbose_level=10,
        minimum_iterations=min_it
    )

    for i in range(min_it * 2):
        assert solver.check_should_stop(i) == False
    sleep(time_crit.total_seconds * 1.1)
    assert solver.check_should_stop(123) == True

def test_one_improvement_stoppage_criterion():
    improvement_crit = ImprovementStopCriterion(0.1)
    min_it = 10
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[improvement_crit],
        population_size=100,
        verbose_level=10,
        minimum_iterations=min_it
    )

    result = 1000.
    modifier = .99 - improvement_crit.min_improvement
    for _ in range(min_it * 2):
        assert solver.check_should_stop(result) == False
        result *= modifier
    assert solver.check_should_stop(result) == False
    assert solver.check_should_stop(result) == True

def test_multiple_stoppage_criteria():
    min_it = 3
    it_crit = IterationsStopCriterion(2 * min_it)
    time_crit = TimeStopCriterion(100.)
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[it_crit, time_crit],
        population_size=100,
        verbose_level=10,
        minimum_iterations=min_it
    )

    for i in range(it_crit.total_iterations):
        assert solver.check_should_stop(i) == False
    assert solver.check_should_stop(123) == True
    assert it_crit.current_iteration == it_crit.total_iterations + 1
    assert time_crit.elapsed_time < time_crit.total_seconds

def test_multiple_stoppage_criteria_2():
    min_it = 3
    it_crit = IterationsStopCriterion(2 * min_it)
    time_crit = TimeStopCriterion(.0000000000001)
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=1),
        crossover=OrderCrossover(0.3),
        stop_criterions=[it_crit, time_crit],
        population_size=100,
        verbose_level=10,
        minimum_iterations=min_it
    )

    for i in range(min_it):
        assert solver.check_should_stop(i) == False
    assert solver.check_should_stop(123) == True
    assert it_crit.current_iteration < it_crit.total_iterations
    assert time_crit.elapsed_time > time_crit.total_seconds

def test_create_new_generation():
    population_size = 6
    solver = EvolutionarySolver(
        elite_selector=EliteSelector(ManhattanCostCalculation, elite_size=2),
        crossover=OrderCrossover(0.3),
        stop_criterions=[],
        population_size=population_size,
        verbose_level=10,
        minimum_iterations=10
    )
    generation = [[0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 0, 1]]
    costs = solver.elite_selector.calculate_cost(TEST_COORDINATES, generation)
    elite = [(generation[i], costs[i]) for i in range(len(generation))]
    new_gen = solver.create_new_generation(elite)
    assert len(new_gen) == population_size
    assert generation[0] in new_gen
    assert generation[1] in new_gen