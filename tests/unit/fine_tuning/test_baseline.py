import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from src.fine_tuning.baseline import load_baseline_result

def test_load_baseline_result_success():
    """Test successful baseline loading."""
    baseline_content = """
Some header content
DATA_LOADING_TIME [s]: 0.001
PROCESSING_TIME [s]: 0.002
TOTAL_DISTANCE_CALCULATED: 2579.0
"""
    
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=baseline_content)):
        result = load_baseline_result("test.tsp")
        assert result == 2579.0

def test_load_baseline_result_file_not_found():
    """Test baseline loading when file doesn't exist."""
    with patch('pathlib.Path.exists', return_value=False):
        result = load_baseline_result("nonexistent.tsp")
        assert result is None

def test_load_baseline_result_no_distance():
    """Test baseline loading when TOTAL_DISTANCE_CALCULATED is missing."""
    baseline_content = """
Some header content
DATA_LOADING_TIME [s]: 0.001
PROCESSING_TIME [s]: 0.002
"""
    
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=baseline_content)):
        result = load_baseline_result("test.tsp")
        assert result is None

def test_load_baseline_result_malformed_distance():
    """Test baseline loading with malformed distance value."""
    baseline_content = """
TOTAL_DISTANCE_CALCULATED: invalid_number
"""
    
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=baseline_content)):
        result = load_baseline_result("test.tsp")
        assert result is None

def test_load_baseline_result_file_read_error():
    """Test baseline loading when file read fails."""
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', side_effect=IOError("File read error")):
        result = load_baseline_result("test.tsp")
        assert result is None

def test_load_baseline_result_decimal_distance():
    """Test baseline loading with decimal distance."""
    baseline_content = """
TOTAL_DISTANCE_CALCULATED: 1234.567
"""
    
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=baseline_content)):
        result = load_baseline_result("test.tsp")
        assert result == pytest.approx(1234.567)

def test_load_baseline_result_multiple_matches():
    """Test baseline loading with multiple TOTAL_DISTANCE_CALCULATED entries."""
    baseline_content = """
TOTAL_DISTANCE_CALCULATED: 1000.0
Some other content
TOTAL_DISTANCE_CALCULATED: 2000.0
"""
    
    with patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=baseline_content)):
        result = load_baseline_result("test.tsp")
        # Should match the first occurrence
        assert result == 1000.0
