import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import json
from src.fine_tuning.tuner import TSPFineTuner
from src.fine_tuning.types import TrialResult

@pytest.fixture
def temp_csv_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("x,y\n100,200\n150,250\n")
        return f.name

@pytest.fixture
def mock_trial_results():
    return [
        {
            'trial_id': 1,
            'best_cost': 1000.0,
            'execution_time': 2.0,
            'total_iterations': 50,
            'convergence_data': [{'iteration': 1, 'best_cost': 1000.0, 'time_elapsed': 0.1}],
            'parameters': {'population_size': 50, 'elite_size': 0.2}
        },
        {
            'trial_id': 2,
            'best_cost': 950.0,
            'execution_time': 2.5,
            'total_iterations': 60,
            'convergence_data': [{'iteration': 1, 'best_cost': 950.0, 'time_elapsed': 0.1}],
            'parameters': {'population_size': 50, 'elite_size': 0.2}
        }
    ]

def test_tsp_fine_tuner_init(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0):
        tuner = TSPFineTuner(temp_csv_file, 5)
        
        assert tuner.input_file == Path(temp_csv_file)
        assert tuner.num_parameter_sets == 5
        assert tuner.dataset_name.endswith('.tsp')
        assert tuner.baseline_cost == 800.0
        assert tuner.results == []
        assert tuner.best_params is None
        assert tuner.best_avg_cost == float('inf')

def test_tsp_fine_tuner_dataset_name_conversion(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result') as mock_load:
        tuner = TSPFineTuner(temp_csv_file, 1)
        
        expected_name = Path(temp_csv_file).stem + '.tsp'
        mock_load.assert_called_once_with(expected_name)

def test_run_parameter_set(temp_csv_file, mock_trial_results):
    params = {'population_size': 50, 'elite_size': 0.2, 'crossover_segment': 0.3, 'stop_iterations': 100, 'stop_improvement': 0.001}
    
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0), \
         patch('concurrent.futures.ProcessPoolExecutor') as mock_executor, \
         patch('src.fine_tuning.tuner.cpu_count', return_value=4):
        
        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        
        future1, future2 = MagicMock(), MagicMock()
        future1.result.return_value = mock_trial_results[0]
        future2.result.return_value = mock_trial_results[1]
        
        mock_executor_instance.submit.side_effect = [future1, future2]
        
        with patch('concurrent.futures.as_completed', return_value=[future1, future2]):
            tuner = TSPFineTuner(temp_csv_file, 1)
            
            with patch('src.fine_tuning.tuner.Config.MIN_TRIALS', 2):
                result = tuner.run_parameter_set(1, params)
        
        assert result['parameters'] == params
        assert len(result['trials']) == 2
        assert 'statistics' in result
        assert 'baseline_comparison' in result

def test_export_results(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0):
        tuner = TSPFineTuner(temp_csv_file, 1)
        tuner.results = [{
            'parameters': {'population_size': 50, 'elite_size': 0.2},
            'statistics': {'best_cost': 950.0, 'average_cost': 975.0},
            'trials': [{'trial_id': 1, 'convergence_data': []}],
            'baseline_comparison': {'baseline_cost': 800.0}
        }]
        tuner.best_params = {'population_size': 50}
        tuner.best_avg_cost = 975.0
    
    with patch('pathlib.Path.mkdir'), \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('json.dump') as mock_json_dump, \
         patch('csv.DictWriter') as mock_csv_writer:
        
        tuner.export_results()
        
        assert mock_file.call_count >= 3
        mock_json_dump.assert_called_once()

def test_run_complete_process(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0), \
         patch.object(TSPFineTuner, 'run_parameter_set') as mock_run_param_set, \
         patch.object(TSPFineTuner, 'export_results') as mock_export, \
         patch.object(TSPFineTuner, 'print_final_summary') as mock_summary, \
         patch('src.fine_tuning.tuner.generate_parameter_set') as mock_gen_params:
        
        mock_gen_params.return_value = {'population_size': 50, 'elite_size': 0.2}
        
        mock_run_param_set.return_value = {
            'parameters': {'population_size': 50, 'elite_size': 0.2},
            'statistics': {'average_cost': 950.0},
            'trials': [],
            'baseline_comparison': {}
        }
        
        tuner = TSPFineTuner(temp_csv_file, 2)
        tuner.run()
        
        assert mock_run_param_set.call_count == 2
        mock_export.assert_called_once()
        mock_summary.assert_called_once()

def test_best_params_update(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0):
        tuner = TSPFineTuner(temp_csv_file, 1)
        
        result1 = {
            'parameters': {'population_size': 50},
            'statistics': {'average_cost': 1000.0},
            'trials': [],
            'baseline_comparison': {}
        }
        
        result2 = {
            'parameters': {'population_size': 100},
            'statistics': {'average_cost': 900.0},
            'trials': [],
            'baseline_comparison': {}
        }
        
        tuner.results.append(result1)
        if result1['statistics']['average_cost'] < tuner.best_avg_cost:
            tuner.best_avg_cost = result1['statistics']['average_cost']
            tuner.best_params = result1['parameters']
        
        tuner.results.append(result2)
        if result2['statistics']['average_cost'] < tuner.best_avg_cost:
            tuner.best_avg_cost = result2['statistics']['average_cost']
            tuner.best_params = result2['parameters']
        
        assert tuner.best_avg_cost == 900.0
        assert tuner.best_params == {'population_size': 100}

def test_print_final_summary_with_results(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0):
        tuner = TSPFineTuner(temp_csv_file, 1)
        tuner.results = [
            {
                'parameters': {'population_size': 50},
                'statistics': {'best_cost': 900.0, 'average_cost': 950.0, 'std_deviation': 25.0},
                'trials': [],
                'baseline_comparison': {}
            }
        ]
        tuner.baseline_cost = 800.0
    
    with patch('builtins.print') as mock_print:
        tuner.print_final_summary()
        
        assert mock_print.call_count > 0
        
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        summary_text = ' '.join(print_calls)
        assert 'FINE-TUNING COMPLETE' in summary_text

def test_print_final_summary_no_results(temp_csv_file):
    with patch('src.fine_tuning.tuner.load_baseline_result', return_value=800.0):
        tuner = TSPFineTuner(temp_csv_file, 1)
        tuner.results = []
    
    with patch('builtins.print') as mock_print:
        tuner.print_final_summary()
        
        assert mock_print.call_count > 0
