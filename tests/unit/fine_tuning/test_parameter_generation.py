import pytest
from unittest.mock import patch
from src.fine_tuning.parameter_generation import generate_parameter_set
from src.fine_tuning.config import Config

def test_generate_parameter_set_defaults():
    params = generate_parameter_set()
    
    assert params == Config.DEFAULT_PARAMS

def test_generate_parameter_set_with_best_params():
    best_params = {
        'population_size': 100,
        'elite_size': 0.15,
        'crossover_segment': 0.25,
        'stop_iterations': 150,
        'stop_improvement': 0.005
    }
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.5), \
         patch('src.fine_tuning.parameter_generation.random.gauss', return_value=0.1), \
         patch('src.fine_tuning.parameter_generation.random.uniform', return_value=0.3):
        
        params = generate_parameter_set(best_params)
        
        for param, value in params.items():
            min_val, max_val = Config.PARAM_RANGES[param]
            assert min_val <= value <= max_val

def test_generate_parameter_set_exploitation():
    best_params = {
        'population_size': 100,
        'elite_size': 0.05,  # Within valid range (0.01, 0.1)
        'crossover_segment': 0.25,
        'stop_iterations': 150,
        'stop_improvement': 0.005
    }
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.5), \
         patch('src.fine_tuning.parameter_generation.random.gauss', return_value=0.0):
        
        params = generate_parameter_set(best_params)
        
        assert params['population_size'] == 100
        assert params['elite_size'] == pytest.approx(0.05)

def test_generate_parameter_set_exploration():
    best_params = {
        'population_size': 100,
        'elite_size': 0.05,  # Within valid range (0.01, 0.1)
        'crossover_segment': 0.25,
        'stop_iterations': 150,
        'stop_improvement': 0.005
    }
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.8), \
         patch('src.fine_tuning.parameter_generation.random.uniform') as mock_uniform:
        
        mock_uniform.side_effect = [150, 0.05, 0.2, 200, 0.0005]  # Updated to valid ranges
        
        params = generate_parameter_set(best_params)
        
        assert params['population_size'] == 150
        assert params['elite_size'] == pytest.approx(0.05)
        assert params['crossover_segment'] == pytest.approx(0.2)
        assert params['stop_iterations'] == 200
        assert params['stop_improvement'] == pytest.approx(0.0005)

def test_generate_parameter_set_integer_conversion():
    best_params = Config.DEFAULT_PARAMS.copy()
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.5), \
         patch('src.fine_tuning.parameter_generation.random.gauss', return_value=10.7):
        
        params = generate_parameter_set(best_params)
        
        for param in Config.INTEGER_PARAMS:
            assert isinstance(params[param], int)

def test_generate_parameter_set_range_clamping():
    best_params = {
        'population_size': 20,
        'elite_size': 0.4,
        'crossover_segment': 0.1,
        'stop_iterations': 50,
        'stop_improvement': 0.01
    }
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.5), \
         patch('src.fine_tuning.parameter_generation.random.gauss', return_value=1000):
        
        params = generate_parameter_set(best_params)
        
        for param, value in params.items():
            min_val, max_val = Config.PARAM_RANGES[param]
            assert min_val <= value <= max_val

def test_generate_parameter_set_negative_clamping():
    best_params = Config.DEFAULT_PARAMS.copy()
    
    with patch('src.fine_tuning.parameter_generation.random.random', return_value=0.5), \
         patch('src.fine_tuning.parameter_generation.random.gauss', return_value=-1000):
        
        params = generate_parameter_set(best_params)
        
        for param, value in params.items():
            min_val, max_val = Config.PARAM_RANGES[param]
            assert value >= min_val

def test_generate_parameter_set_all_params_present():
    params = generate_parameter_set()
    
    expected_params = set(Config.PARAM_RANGES.keys())
    assert set(params.keys()) == expected_params
