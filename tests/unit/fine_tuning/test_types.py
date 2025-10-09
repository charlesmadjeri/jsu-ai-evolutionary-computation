import pytest
from src.fine_tuning.types import TrialResult, ParameterSetResult

def test_trial_result_structure():
    trial_result: TrialResult = {
        'trial_id': 1,
        'best_cost': 1234.56,
        'execution_time': 45.2,
        'total_iterations': 100,
        'convergence_data': [
            {'iteration': 1, 'best_cost': 1500.0, 'time_elapsed': 0.1},
            {'iteration': 2, 'best_cost': 1234.56, 'time_elapsed': 0.2}
        ],
        'parameters': {
            'population_size': 50,
            'elite_size': 0.2,
            'crossover_segment': 0.3,
            'stop_iterations': 100,
            'stop_improvement': 0.001
        }
    }
    
    assert 'trial_id' in trial_result
    assert 'best_cost' in trial_result
    assert 'execution_time' in trial_result
    assert 'total_iterations' in trial_result
    assert 'convergence_data' in trial_result
    assert 'parameters' in trial_result
    
    assert isinstance(trial_result['trial_id'], int)
    assert isinstance(trial_result['best_cost'], (float, int))
    assert isinstance(trial_result['execution_time'], (float, int))
    assert isinstance(trial_result['total_iterations'], int)
    assert isinstance(trial_result['convergence_data'], list)
    assert isinstance(trial_result['parameters'], dict)

def test_parameter_set_result_structure():
    
    parameter_set_result: ParameterSetResult = {
        'parameters': {
            'population_size': 50,
            'elite_size': 0.2,
            'crossover_segment': 0.3,
            'stop_iterations': 100,
            'stop_improvement': 0.001
        },
        'trials': [
            {
                'trial_id': 1,
                'best_cost': 1234.56,
                'execution_time': 45.2,
                'total_iterations': 100,
                'convergence_data': [],
                'parameters': {'population_size': 50, 'elite_size': 0.2}
            }
        ],
        'statistics': {
            'best_cost': 1234.56,
            'average_cost': 1300.0,
            'std_deviation': 50.0,
            'average_execution_time': 45.2,
            'success_rate': 1.0,
            'baseline_gap_best_percent': 15.2,
            'baseline_gap_average_percent': 18.5
        },
        'baseline_comparison': {
            'baseline_cost': 1000.0,
            'dataset_name': 'test.tsp'
        }
    }
    
    assert 'parameters' in parameter_set_result
    assert 'trials' in parameter_set_result
    assert 'statistics' in parameter_set_result
    assert 'baseline_comparison' in parameter_set_result
    
    assert isinstance(parameter_set_result['parameters'], dict)
    assert isinstance(parameter_set_result['trials'], list)
    assert isinstance(parameter_set_result['statistics'], dict)
    assert isinstance(parameter_set_result['baseline_comparison'], dict)
    
    if parameter_set_result['trials']:
        trial = parameter_set_result['trials'][0]
        assert 'trial_id' in trial
        assert 'best_cost' in trial
        assert 'execution_time' in trial

def test_trial_result_with_convergence_data():
    
    convergence_data = [
        {'iteration': 1, 'best_cost': 2000.0, 'time_elapsed': 0.05},
        {'iteration': 2, 'best_cost': 1800.0, 'time_elapsed': 0.10},
        {'iteration': 3, 'best_cost': 1600.0, 'time_elapsed': 0.15},
        {'iteration': 4, 'best_cost': 1500.0, 'time_elapsed': 0.20}
    ]
    
    trial_result: TrialResult = {
        'trial_id': 5,
        'best_cost': 1500.0,
        'execution_time': 2.5,
        'total_iterations': 4,
        'convergence_data': convergence_data,
        'parameters': {'population_size': 100, 'elite_size': 0.15}
    }
    
    assert len(trial_result['convergence_data']) == 4
    for i, point in enumerate(trial_result['convergence_data']):
        assert point['iteration'] == i + 1
        assert 'best_cost' in point
        assert 'time_elapsed' in point

def test_empty_trial_result():
    
    trial_result: TrialResult = {
        'trial_id': 0,
        'best_cost': float('inf'),
        'execution_time': 0.0,
        'total_iterations': 0,
        'convergence_data': [],
        'parameters': {}
    }
    
    assert trial_result['trial_id'] == 0
    assert trial_result['best_cost'] == float('inf')
    assert len(trial_result['convergence_data']) == 0
    assert len(trial_result['parameters']) == 0
