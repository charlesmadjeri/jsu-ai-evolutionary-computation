import pytest
import subprocess
from unittest.mock import patch, MagicMock
from src.fine_tuning.solver_interface import (
    parse_solver_output,
    build_solver_command,
    run_single_trial
)

def test_parse_solver_output_complete():
    output = """
Some initial output
SOLVER_START: Starting algorithm
FINAL_RESULT_START
BEST_COST: 1234.56
EXECUTION_TIME: 45.123
TOTAL_ITERATIONS: 100
CONVERGENCE_DATA: [{"iteration": 1, "best_cost": 1500.0, "time_elapsed": 0.1}, {"iteration": 2, "best_cost": 1234.56, "time_elapsed": 0.2}]
FINAL_RESULT_END
Some final output
"""
    
    result = parse_solver_output(output)
    
    assert result['best_cost'] == pytest.approx(1234.56)
    assert result['execution_time'] == pytest.approx(45.123)
    assert result['total_iterations'] == 100
    assert len(result['convergence_data']) == 2
    assert result['convergence_data'][0]['iteration'] == 1

def test_parse_solver_output_partial():
    output = """
FINAL_RESULT_START
BEST_COST: 999.0
EXECUTION_TIME: 30.0
FINAL_RESULT_END
"""
    
    result = parse_solver_output(output)
    
    assert result['best_cost'] == pytest.approx(999.0)
    assert result['execution_time'] == pytest.approx(30.0)
    assert result['total_iterations'] is None
    assert result['convergence_data'] == []

def test_parse_solver_output_malformed():
    output = """
FINAL_RESULT_START
BEST_COST: invalid_number
EXECUTION_TIME: also_invalid
TOTAL_ITERATIONS: not_a_number
CONVERGENCE_DATA: {invalid json}
FINAL_RESULT_END
"""
    
    result = parse_solver_output(output)
    
    assert result['best_cost'] is None
    assert result['execution_time'] is None
    assert result['total_iterations'] is None
    assert result['convergence_data'] == []

def test_parse_solver_output_no_result_block():
    output = """
Some output without result block
BEST_COST: 1000.0
EXECUTION_TIME: 10.0
"""
    
    result = parse_solver_output(output)
    
    assert result['best_cost'] is None
    assert result['execution_time'] is None
    assert result['total_iterations'] is None
    assert result['convergence_data'] == []

def test_build_solver_command():
    params = {
        'population_size': 100,
        'elite_size': 0.15,
        'crossover_segment': 0.25,
        'stop_iterations': 200,
        'stop_improvement': 0.001
    }
    
    cmd = build_solver_command('data/test.csv', params)
    
    expected_cmd = [
        'python3', 'src/main.py',
        '-ps', '100',
        '-es', '0.15',
        '-cr', 'order',
        '-cs', '0.25',
        '-sit', '200',
        '-sim', '0.001',
        '-cc', 'manhattan',
        '--verbose', '1',
        'data/test.csv'
    ]
    
    assert cmd == expected_cmd

def test_build_solver_command_float_population():
    params = {
        'population_size': 100.0,
        'elite_size': 0.2,
        'crossover_segment': 0.3,
        'stop_iterations': 150,
        'stop_improvement': 0.005
    }
    
    cmd = build_solver_command('data/test.csv', params)
    
    assert cmd[3] == '100'  # -ps value

def test_run_single_trial_success():
    args = (1, 'data/test.csv', {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001})
    
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = """
FINAL_RESULT_START
BEST_COST: 1500.0
EXECUTION_TIME: 25.5
TOTAL_ITERATIONS: 80
CONVERGENCE_DATA: []
FINAL_RESULT_END
"""
    
    with patch('subprocess.run', return_value=mock_result):
        result = run_single_trial(args)
    
    assert result['trial_id'] == 1
    assert result['best_cost'] == pytest.approx(1500.0)
    assert result['execution_time'] == pytest.approx(25.5)
    assert result['total_iterations'] == 80
    assert result['parameters'] == args[2]

def test_run_single_trial_failure():
    args = (2, 'data/test.csv', {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001})
    
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "Algorithm failed"
    
    with patch('subprocess.run', return_value=mock_result):
        result = run_single_trial(args)
    
    assert result['trial_id'] == 2
    assert result['best_cost'] == float('inf')
    assert result['total_iterations'] == 0
    assert result['convergence_data'] == []

def test_run_single_trial_timeout():
    args = (3, 'data/test.csv', {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001})
    
    with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('cmd', 300)):
        result = run_single_trial(args)
    
    assert result['trial_id'] == 3
    assert result['best_cost'] == float('inf')
    assert result['execution_time'] == 300  # ALGORITHM_TIMEOUT

def test_run_single_trial_exception():
    args = (4, 'data/test.csv', {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001})
    
    with patch('subprocess.run', side_effect=Exception("Unexpected error")):
        result = run_single_trial(args)
    
    assert result['trial_id'] == 4
    assert result['best_cost'] == float('inf')
    assert result['total_iterations'] == 0

def test_run_single_trial_parsing_failure():
    args = (5, 'data/test.csv', {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001})
    
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Invalid output format"
    
    with patch('subprocess.run', return_value=mock_result):
        result = run_single_trial(args)
    
    assert result['trial_id'] == 5
    assert result['best_cost'] == float('inf')
