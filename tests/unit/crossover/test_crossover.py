import pytest

from src.crossover.crossover import Crossover

parents = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9], 
    [4, 5, 2, 1, 8, 7, 6, 3, 9]
)
crossover_size_rate = 0.3

def test_crossover_init():    
    with pytest.raises(TypeError):
        crossover = Crossover(parents, crossover_size_rate)
        assert crossover.parents == parents
        assert crossover.crossover_size_rate == crossover_size_rate

def test_crossover_crossover():
    with pytest.raises(TypeError):
        crossover = Crossover(parents, crossover_size_rate)
        crossover.crossover()

def test_crossover_get_cross_points():
    with pytest.raises(TypeError):
        crossover = Crossover(parents, crossover_size_rate)
        crossover.get_cross_points(len(parents[0]))

def test_crossover_abstract_methods():
    class TestCrossover(Crossover):
        def __init__(self, parents, crossover_size_rate):
            super().__init__(parents, crossover_size_rate)
        
        def crossover(self) -> tuple[list[int], list[int]]:
            return super().crossover()
        
        def get_cross_points(self, cities_nb) -> tuple[int, int]:
            return super().get_cross_points(cities_nb)
    
    crossover = TestCrossover(parents, crossover_size_rate)
    
    # Both functions should return None as they only overwrite the abstract methods
    assert crossover.crossover() == None
    assert isinstance(crossover.get_cross_points(len(parents[0])), tuple)
    assert len(crossover.get_cross_points(len(parents[0]))) == 2
    assert all(isinstance(i, int) for i in crossover.get_cross_points(len(parents[0])))



