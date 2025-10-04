from random import sample, shuffle
from src.crossover.order_crossover import OrderCrossover

parents = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9], 
    [4, 5, 2, 1, 8, 7, 6, 3, 9]
)
segment_length = 3

def test_order_crossover_init():
    crossover = OrderCrossover(segment_length)
    assert crossover.get_segment_length(9999999999) == segment_length

def test_order_crossover_init_random_segment_length():
    crossover = OrderCrossover(None)
    l = 5
    segment_length = crossover.get_segment_length(l)
    # one different
    for i in range(1000):
        generated = crossover.get_segment_length(l)
        if generated != segment_length:
            break
    else:
        assert False
    assert generated != segment_length

    # one same
    for i in range(1000):
        generated = crossover.get_segment_length(l)
        if generated == segment_length:
            break
    else:
        assert False
    assert generated == segment_length


def test_order_crossover_get_cross_points():
    crossover = OrderCrossover(segment_length)
    idx_a, idx_b = crossover.get_cross_points(len(parents[0]))
    assert 0 <= idx_a < idx_b <= len(parents[0])
    assert idx_b - idx_a == int(segment_length)

def test_order_crossover_crossover():
    crossover = OrderCrossover(segment_length)
    par_a, par_b = tuple(parents)
    child_a, child_b = crossover.crossover(parents)
    
    assert len(parents[0]) == len(parents[1])
    assert sorted(parents[0]) == sorted(parents[1])

    assert sorted(child_a) == sorted(par_a)
    assert sorted(child_b) == sorted(par_b)

def test_unique_cities():
    solution_size = 100
    iterations = 1000
    for i in range(0, iterations):
        parent1 = list(range(0, solution_size))
        shuffle(parent1)
        parent2 = parent1.copy()
        while True:
            shuffle(parent2)
            if parent2 != parent1:
                break
        parent1_copy = parent1.copy()
        parent2_copy = parent2.copy()
        crossover = OrderCrossover(segment_length)
        offspring1, offspring2 = crossover.crossover((parent1, parent2))
        assert parent1_copy == parent1
        assert parent2_copy == parent2
        assert len(set(offspring1)) == solution_size
        assert len(set(offspring2)) == solution_size
        assert min(offspring1) == 0
        assert max(offspring1) == solution_size - 1
        assert min(offspring2) == 0
        assert max(offspring2) == solution_size - 1