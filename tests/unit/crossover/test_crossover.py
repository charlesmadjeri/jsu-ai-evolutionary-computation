import pytest

from crossover.crossover import Crossover

parents = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9], 
    [4, 5, 2, 1, 8, 7, 6, 3, 9]
)
segment_length = 3

def test_crossover_init():    
    with pytest.raises(TypeError):
        crossover = Crossover(segment_length)
        assert crossover.segment_length == segment_length

def test_crossover_crossover():
    with pytest.raises(TypeError):
        crossover = Crossover(segment_length)
        crossover.crossover(parents)

def test_crossover_get_cross_points():
    with pytest.raises(TypeError):
        crossover = Crossover(segment_length)
        crossover.get_cross_points(len(parents[0]))

def test_crossover_abstract_methods():
    class TestCrossover(Crossover):
        def __init__(self, segment_length):
            super().__init__(segment_length)
        
        def crossover(self, parents) -> tuple[list[int], list[int]]:
            return super().crossover(parents)
        
        def get_cross_points(self, cities_nb) -> tuple[int, int]:
            return super().get_cross_points(cities_nb)
    
    crossover = TestCrossover(segment_length)
    
    # Both functions should return None as they only overwrite the abstract methods
    assert crossover.crossover(parents) == None
    assert isinstance(crossover.get_cross_points(len(parents[0])), tuple)
    assert len(crossover.get_cross_points(len(parents[0]))) == 2
    assert all(isinstance(i, int) for i in crossover.get_cross_points(len(parents[0])))



