import time
import pytest
from src.stop_criterions.improvement_stop_criterion import ImprovementStopCriterion
from src.stop_criterions.iterations_stop_criterion import IterationsStopCriterion
from src.stop_criterions.time_stop_criterion import TimeStopCriterion

def test_improvement_stop_criterion():
    """Test improvement stop criterion - 10% improvement."""
    min_improvement = .10
    min_modifier = 1. - min_improvement
    improvement_stop_criterion = ImprovementStopCriterion(min_improvement)
    """Case 1: Stopping because of too small improvement."""
    assert improvement_stop_criterion.previous_distance == None
    assert improvement_stop_criterion.check_continue(1000.) == True
    assert improvement_stop_criterion.previous_distance == pytest.approx(1000.)
    assert improvement_stop_criterion.check_continue(improvement_stop_criterion.previous_distance) == False
    improvement_stop_criterion.restart()
    assert improvement_stop_criterion.previous_distance == None
    assert improvement_stop_criterion.check_continue(100.) == True
    assert improvement_stop_criterion.check_continue(improvement_stop_criterion.previous_distance * min_modifier - 1.) == True
    assert improvement_stop_criterion.check_continue(improvement_stop_criterion.previous_distance * min_modifier - 5.) == True
    assert improvement_stop_criterion.check_continue(improvement_stop_criterion.previous_distance * min_modifier + 1.) == False
    """Case 2: Throw exception on bad initialization."""
    with pytest.raises(AssertionError):
        ImprovementStopCriterion(0.)
    with pytest.raises(AssertionError):
        ImprovementStopCriterion(-1.)
    """Case 3: Test string representation."""
    str_repr = str(improvement_stop_criterion)
    assert str_repr != ""
    assert str(min_improvement) in str_repr
    assert str(improvement_stop_criterion.min_improvement) in str_repr
    assert str(improvement_stop_criterion.improvement) in str_repr
    

def test_iterations_stop_criterion():
    """Test iterations stop criterion - 10 iterations."""
    total_iterations = 3
    iterations_stop_criterion = IterationsStopCriterion(total_iterations)
    """Case 1: Stopping because of too many iterations."""
    for i in range(total_iterations):
        assert iterations_stop_criterion.check_continue(1234.) == True
    assert iterations_stop_criterion.check_continue(1234.) == False
    iterations_stop_criterion.restart()
    for i in range(total_iterations):
        assert iterations_stop_criterion.check_continue(1234.) == True
    assert iterations_stop_criterion.check_continue(1234.) == False
    """Case 2: Throw exception on bad initialization."""
    with pytest.raises(AssertionError):
        IterationsStopCriterion(0)
    with pytest.raises(AssertionError):
        IterationsStopCriterion(-1)
    """Case 3: Test string representation."""
    str_repr = str(iterations_stop_criterion)
    assert str_repr != ""
    assert str(total_iterations) in str_repr
    assert str(iterations_stop_criterion.current_iteration) in str_repr
    assert str(iterations_stop_criterion.total_iterations) in str_repr

def test_time_stop_criterion():
    """Test time stop criterion - 1 second"""
    sleep_time = 0.2
    time_stop_criterion = TimeStopCriterion(sleep_time)
    """Case 1: Stopping because of too much time."""
    assert time_stop_criterion.check_continue(1234.) == True
    time.sleep(sleep_time * 0.4)
    assert time_stop_criterion.check_continue(1234.) == True
    time.sleep(sleep_time * 0.4)
    assert time_stop_criterion.check_continue(1234.) == True
    time.sleep(sleep_time * 0.3)
    assert time_stop_criterion.check_continue(1234.) == False
    time_stop_criterion.restart()
    assert time_stop_criterion.check_continue(1234.) == True
    time.sleep(sleep_time * 0.9)
    assert time_stop_criterion.check_continue(1234.) == True
    time.sleep(sleep_time * 0.2)
    assert time_stop_criterion.check_continue(1234.) == False
    """Case 3: Test string representation."""
    str_repr = str(time_stop_criterion)
    assert str_repr != ""
    assert str(sleep_time) in str_repr
    assert str(time_stop_criterion.elapsed_time) in str_repr
    assert str(time_stop_criterion.total_seconds) in str_repr