from src.elite_selector.elite_selector import EliteSelector
from src.cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation

parents = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8], 
    [3, 4, 1, 0, 7, 6, 5, 2, 8],
    [6, 5, 3, 2, 8, 4, 1, 0, 7],
    [4, 0, 5, 6, 8, 3, 1, 2, 7],
    [1, 3, 0, 7, 4, 5, 2, 6, 8],
    [2, 7, 5, 4, 6, 8, 1, 0, 3],
    [0, 2, 3, 8, 1, 5, 7, 6, 4],
    [7, 0, 6, 8, 3, 4, 5, 1, 2]
]

coord = [
    (7810,6053),
    (7798,5709),
    (7264,5575),
    (7324,5560),
    (7547,5503),
    (7744,5476),
    (7821,5457),
    (7883,5408),
    (7874,5405)
]

elite_size = 4

elite_selector  = EliteSelector(coord, ManhattanCostCalculation, elite_size)

def test_elite_selector_init():
    assert elite_selector.coordinates == coord
    assert elite_selector.cost_calculator == ManhattanCostCalculation
    assert elite_selector.elite_size == elite_size

def test_elite_selector_calculate_cost():
    cost = elite_selector.calculate_cost(parents)
    assert len(cost) == len(elite_selector.coordinates) - 1

def test_elite_selector_find_elite_elements():
    elites = elite_selector.find_elite_elements(parents)
    assert len(elites) == elite_size
    for elite in elites:
        assert elite in parents

def test_elite_selector_elites_are_lowest_cost():
    costs = elite_selector.calculate_cost(parents)
    elites = elite_selector.find_elite_elements(parents)
    elite_costs = [costs[parents.index(elite)] for elite in elites]
    sorted_costs = sorted(costs)[:elite_size]
    assert sorted(elite_costs) == sorted_costs

def test_elite_selector_no_duplicates_in_elites():
    elites = elite_selector.find_elite_elements(parents)
    assert len(elites) == len(set(tuple(elite) for elite in elites))
    

def test_elite_selector_handles_ties():
    tied_parents = [
        [0, 1, 2],
        [0, 1, 2],
        [1, 2, 0],
        [2, 0, 1]
    ]
    tied_coords = [
        (0, 0),
        (1, 0),
        (0, 1)
    ]
    elite_size_tie = 2
    elite_selector_tie = EliteSelector(tied_coords, ManhattanCostCalculation, elite_size_tie)
    elites_tie = elite_selector_tie.find_elite_elements(tied_parents)
    assert len(elites_tie) == elite_size_tie
    for elite in elites_tie:
        assert elite in tied_parents

def test_elite_selector_empty_generation():
    empty_selector = EliteSelector(coord, ManhattanCostCalculation, elite_size)
    elites_empty = empty_selector.find_elite_elements([])
    assert elites_empty == []

def test_cost_calculation_vs_manual():
    cost_calculator = ManhattanCostCalculation
    coordinates = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    elite_selector = EliteSelector(coordinates, cost_calculator, 2)
    generation = [[0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], [2, 3, 4, 5, 0, 1], [4, 3, 2, 1, 0, 5]]
    costs = elite_selector.calculate_cost(generation)
    for i in range(len(generation)):
        cost = 0
        for j in range(1, len(generation[i])):
            cost += cost_calculator.calculate(coordinates[generation[i][j-1]], coordinates[generation[i][j]])
        print(i, cost, costs[i])
        assert cost == costs[i]