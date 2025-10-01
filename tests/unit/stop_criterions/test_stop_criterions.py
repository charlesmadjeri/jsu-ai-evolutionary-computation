import time
import pytest
from src.stop_criterions.improvement_stop_criterion import ImprovementStopCriterion
from src.stop_criterions.iterations_stop_criterion import IterationsStopCriterion
from src.stop_criterions.time_stop_criterion import TimeStopCriterion

def test_improvement_stop_criterion():
    """Test improvement stop criterion - 10% improvement."""
    improvement_stop_criterion = ImprovementStopCriterion(.10)
    """Case 1: Stopping because of too small improvement."""
    improvement_stop_criterion.start()
    assert improvement_stop_criterion.previous_distance == None
    assert improvement_stop_criterion.check(1000.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(1000.)
    assert improvement_stop_criterion.check(1200.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(1200.)
    assert improvement_stop_criterion.check(1201.) == False
    improvement_stop_criterion.end()
    """Case 2: Stopping because of negative improvement."""
    improvement_stop_criterion.start()
    assert improvement_stop_criterion.previous_distance == None
    assert improvement_stop_criterion.check(100.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(100.)
    assert improvement_stop_criterion.check(120.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(120.)
    assert improvement_stop_criterion.check(140.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(140.)
    assert improvement_stop_criterion.check(90.) == False
    improvement_stop_criterion.end()
    """Case 3: Throw exception on bad initialization."""
    with pytest.raises(AssertionError):
        ImprovementStopCriterion(0.)
    with pytest.raises(AssertionError):
        ImprovementStopCriterion(-1.)


def test_iterations_stop_criterion():
    """Test iterations stop criterion - 10 iterations."""
    iterations_stop_criterion = IterationsStopCriterion(10)
    """Case 1: Stopping because of too many iterations."""
    iterations_stop_criterion.start()
    for i in range(10):
        assert iterations_stop_criterion.check(1234.) == True
    assert iterations_stop_criterion.check(1234.) == False
    iterations_stop_criterion.end()
    """Case 2: Throw exception on bad initialization."""
    with pytest.raises(AssertionError):
        IterationsStopCriterion(0)
    with pytest.raises(AssertionError):
        IterationsStopCriterion(-1)

def test_time_stop_criterion():
    """Test time stop criterion - 1 second"""
    time_stop_criterion = TimeStopCriterion(1)
    """Case 1: Stopping because of too much time."""
    time_stop_criterion.start()
    assert time_stop_criterion.check(1234.) == True
    time.sleep(0.25)
    assert time_stop_criterion.check(1234.) == True
    time.sleep(0.25)
    assert time_stop_criterion.check(1234.) == True
    time.sleep(0.6)
    assert time_stop_criterion.check(1234.) == False
    time_stop_criterion.end()