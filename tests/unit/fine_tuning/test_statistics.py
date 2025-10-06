import pytest
from src.fine_tuning.statistics import calculate_statistics
from src.fine_tuning.types import TrialResult

def create_trial_result(trial_id: int, best_cost: float, execution_time: float = 1.0) -> TrialResult:
    return {
        'trial_id': trial_id,
        'best_cost': best_cost,
        'execution_time': execution_time,
        'total_iterations': 100,
        'convergence_data': [],
        'parameters': {'population_size': 50, 'elite_size': 0.2}
    }

def test_calculate_statistics_normal_case():
    trials = [
        create_trial_result(1, 100.0, 1.5),
        create_trial_result(2, 110.0, 2.0),
        create_trial_result(3, 90.0, 1.0),
        create_trial_result(4, 105.0, 1.8),
        create_trial_result(5, 95.0, 1.2)
    ]
    
    stats = calculate_statistics(trials, baseline_cost=80.0)
    
    assert stats['best_cost'] == 90.0
    assert stats['average_cost'] == pytest.approx(100.0)
    assert stats['std_deviation'] > 0
    assert stats['average_execution_time'] == pytest.approx(1.5)
    assert stats['success_rate'] == 1.0
    assert 'baseline_gap_best_percent' in stats
    assert 'baseline_gap_average_percent' in stats
    
    expected_best_gap = ((90.0 - 80.0) / 80.0) * 100
    expected_avg_gap = ((100.0 - 80.0) / 80.0) * 100
    assert stats['baseline_gap_best_percent'] == pytest.approx(expected_best_gap)
    assert stats['baseline_gap_average_percent'] == pytest.approx(expected_avg_gap)

def test_calculate_statistics_with_failures():
    trials = [
        create_trial_result(1, 100.0),
        create_trial_result(2, float('inf')),
        create_trial_result(3, 90.0),
        create_trial_result(4, float('inf')),
        create_trial_result(5, 95.0)
    ]
    
    stats = calculate_statistics(trials)
    
    assert stats['best_cost'] == 90.0
    assert stats['average_cost'] == pytest.approx(95.0)
    assert stats['success_rate'] == 0.6

def test_calculate_statistics_all_failures():
    trials = [
        create_trial_result(1, float('inf')),
        create_trial_result(2, float('inf')),
        create_trial_result(3, float('inf'))
    ]
    
    stats = calculate_statistics(trials, baseline_cost=100.0)
    
    assert stats['best_cost'] == float('inf')
    assert stats['average_cost'] == float('inf')
    assert stats['std_deviation'] == float('inf')
    assert stats['success_rate'] == 0.0

def test_calculate_statistics_single_trial():
    trials = [create_trial_result(1, 150.0, 2.5)]
    
    stats = calculate_statistics(trials)
    
    assert stats['best_cost'] == 150.0
    assert stats['average_cost'] == 150.0
    assert stats['std_deviation'] == 0.0
    assert stats['average_execution_time'] == 2.5
    assert stats['success_rate'] == 1.0

def test_calculate_statistics_no_baseline():
    trials = [
        create_trial_result(1, 100.0),
        create_trial_result(2, 110.0)
    ]
    
    stats = calculate_statistics(trials, baseline_cost=None)
    
    assert 'baseline_gap_best_percent' not in stats
    assert 'baseline_gap_average_percent' not in stats
    assert stats['best_cost'] == 100.0
    assert stats['average_cost'] == 105.0

def test_calculate_statistics_empty_trials():
    stats = calculate_statistics([])
    
    assert stats['best_cost'] == float('inf')
    assert stats['average_cost'] == float('inf')
    assert stats['success_rate'] == 0.0

def test_calculate_statistics_execution_time():
    trials = [
        create_trial_result(1, 100.0, 1.0),
        create_trial_result(2, 100.0, 2.0),
        create_trial_result(3, 100.0, 3.0)
    ]
    
    stats = calculate_statistics(trials)
    assert stats['average_execution_time'] == pytest.approx(2.0)
