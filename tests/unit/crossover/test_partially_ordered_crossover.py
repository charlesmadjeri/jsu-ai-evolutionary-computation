from src.crossover.partially_mapped_crossover import PartiallyMappedCrossover

parents = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9], 
    [4, 5, 2, 1, 8, 7, 6, 3, 9]
)
crossover_size_rate = 0.3

def test_partially_mapped_crossover_init():
    crossover = PartiallyMappedCrossover(parents, crossover_size_rate)
    assert crossover.parents == parents
    assert crossover.crossover_size_rate == crossover_size_rate

def test_partially_mapped_crossover_get_cross_points():
    crossover = PartiallyMappedCrossover(parents, crossover_size_rate)
    idx_a, idx_b = crossover.get_cross_points(len(parents[0]))
    assert 0 <= idx_a < idx_b <= len(parents[0])
    assert idx_b - idx_a == int(crossover_size_rate * len(parents[0]))

def test_partially_mapped_crossover_crossover():
    crossover = PartiallyMappedCrossover(parents, crossover_size_rate)
    par_a, par_b = tuple(parents)
    child_a, child_b = crossover.crossover()
    
    assert len(parents[0]) == len(parents[1])
    assert sorted(parents[0]) == sorted(parents[1])

    assert sorted(child_a) == sorted(par_a)
    assert sorted(child_b) == sorted(par_b)