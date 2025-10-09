import pytest
from src.fine_tuning.config import Config

def test_config_constants():
    """Test that config constants are properly defined."""
    assert Config.ALGORITHM_TIMEOUT == 300
    assert Config.DEFAULT_HIGH_COST == 10000000000.0
    assert Config.MIN_TRIALS == 25
    
    assert Config.EXPLOITATION_PROBABILITY == 0.7
    assert Config.EXPLORATION_VARIANCE == 0.15

def test_param_ranges():
    """Test parameter ranges are valid."""
    ranges = Config.PARAM_RANGES
    
    # Check all required parameters exist
    required_params = {'population_size', 'elite_size', 'crossover_segment', 
                      'stop_iterations', 'stop_improvement'}
    assert set(ranges.keys()) == required_params
    
    # Check ranges are tuples with min < max
    for param, (min_val, max_val) in ranges.items():
        assert isinstance(min_val, (int, float))
        assert isinstance(max_val, (int, float))
        assert min_val < max_val
        assert min_val > 0  # All parameters should be positive

def test_default_params():
    """Test default parameters are within valid ranges."""
    defaults = Config.DEFAULT_PARAMS
    ranges = Config.PARAM_RANGES
    
    # Check all required parameters have defaults
    assert set(defaults.keys()) == set(ranges.keys())
    
    # Check defaults are within ranges
    for param, default_val in defaults.items():
        min_val, max_val = ranges[param]
        assert min_val <= default_val <= max_val

def test_integer_params():
    """Test integer parameter specification."""
    integer_params = Config.INTEGER_PARAMS
    assert isinstance(integer_params, set)
    assert 'population_size' in integer_params
    assert 'stop_iterations' in integer_params
    
    # Check integer params exist in ranges
    for param in integer_params:
        assert param in Config.PARAM_RANGES

def test_config_types():
    """Test configuration value types."""
    assert isinstance(Config.ALGORITHM_TIMEOUT, int)
    assert isinstance(Config.DEFAULT_HIGH_COST, float)
    assert isinstance(Config.MIN_TRIALS, int)
    assert isinstance(Config.EXPLOITATION_PROBABILITY, float)
    assert isinstance(Config.EXPLORATION_VARIANCE, float)
    
    assert 0 < Config.EXPLOITATION_PROBABILITY < 1
    assert Config.EXPLORATION_VARIANCE > 0
