import csv
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path
from typing import Dict, List, Union

from .baseline import load_baseline_result
from .config import Config
from .parameter_generation import generate_parameter_set
from .solver_interface import run_single_trial
from .statistics import calculate_statistics
from .types import ParameterSetResult, TrialResult

class TSPFineTuner:
    def __init__(self, input_file: str, num_parameter_sets: int):
        self.input_file = Path(input_file)
        self.num_parameter_sets = num_parameter_sets
        self.dataset_name = self.input_file.stem + ".tsp"  # Convert .csv to .tsp for baseline lookup
        self.baseline_cost = load_baseline_result(self.dataset_name)
        self.results: List[ParameterSetResult] = []
        self.best_params = None
        self.best_avg_cost = float('inf')
        
    def run_parameter_set(self, param_set_id: int, params: Dict[str, Union[int, float]]) -> ParameterSetResult:
        """Run multiple trials for a single parameter set.
        
        Args:
            param_set_id: ID of the parameter set being tested
            params: Dictionary of parameters to test
            
        Returns:
            Results for this parameter set
        """
        print(f"\n[PARAMETER SET {param_set_id}/{self.num_parameter_sets}]")
        print(f"Parameters: {params}")
        
        trial_args = []
        for trial_id in range(Config.MIN_TRIALS):
            trial_args.append((trial_id + 1, str(self.input_file), params))
        
        trials = []
        with ProcessPoolExecutor(max_workers=min(cpu_count(), 8)) as executor:
            future_to_trial = {executor.submit(run_single_trial, args): args[0] for args in trial_args}
            
            for future in as_completed(future_to_trial):
                trial_id = future_to_trial[future]
                try:
                    result = future.result()
                    trials.append(result)
                    if result['best_cost'] != float('inf'):
                        print(f"  Trial {trial_id:2d}: Cost={result['best_cost']:.2f}, Time={result['execution_time']:.3f}s")
                    else:
                        print(f"  Trial {trial_id:2d}: FAILED")
                except Exception as e:
                    print(f"  Trial {trial_id:2d}: ERROR - {e}")
        
        stats = calculate_statistics(trials, self.baseline_cost)
        
        print(f"Results: Best={stats['best_cost']:.2f}, Avg={stats['average_cost']:.2f}±{stats['std_deviation']:.2f}")
        if self.baseline_cost:
            print(f"Baseline gap: {stats.get('baseline_gap_best_percent', 0):.1f}% (best), {stats.get('baseline_gap_average_percent', 0):.1f}% (avg)")
        
        return {
            'parameters': params,
            'trials': trials,
            'statistics': stats,
            'baseline_comparison': {
                'baseline_cost': self.baseline_cost,
                'dataset_name': self.dataset_name
            }
        }
    
    def export_results(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        results_dir = Path(f"results/fine-tuning/{timestamp}")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        json_file = results_dir / f"fine_tuning_{self.dataset_name}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'metadata': {
                    'dataset': str(self.input_file),
                    'dataset_name': self.dataset_name,
                    'baseline_cost': self.baseline_cost,
                    'num_parameter_sets': self.num_parameter_sets,
                    'trials_per_set': Config.MIN_TRIALS,
                    'timestamp': timestamp,
                    'best_parameters': self.best_params,
                    'best_average_cost': self.best_avg_cost
                },
                'results': self.results
            }, f, indent=2)
        
        csv_file = results_dir / f"summary_{self.dataset_name}.csv"
        with open(csv_file, 'w', newline='') as f:
            fieldnames = [
                'parameter_set_id',
                'population_size', 'elite_size', 'crossover_segment', 'stop_iterations', 'stop_improvement',
                'best_cost', 'average_cost', 'std_deviation', 'average_execution_time', 'success_rate',
                'baseline_gap_best_percent', 'baseline_gap_average_percent'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, result in enumerate(self.results):
                row = {'parameter_set_id': i + 1}
                row.update(result['parameters'])
                row.update(result['statistics'])
                writer.writerow(row)
        
        convergence_file = results_dir / f"convergence_{self.dataset_name}.csv"
        with open(convergence_file, 'w', newline='') as f:
            fieldnames = ['parameter_set_id', 'trial_id', 'iteration', 'best_cost', 'time_elapsed']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for param_set_id, result in enumerate(self.results):
                for trial in result['trials']:
                    for point in trial['convergence_data']:
                        writer.writerow({
                            'parameter_set_id': param_set_id + 1,
                            'trial_id': trial['trial_id'],
                            'iteration': point['iteration'],
                            'best_cost': point['best_cost'],
                            'time_elapsed': point['time_elapsed']
                        })
        
        print(f"\n[EXPORT COMPLETE]")
        print(f"Results folder: {results_dir}")
        print(f"  - Detailed JSON: {json_file.name}")
        print(f"  - Summary CSV: {csv_file.name}")
        print(f"  - Convergence CSV: {convergence_file.name}")
    
    def run(self):
        """Run fullfine-tuning process."""
        print(f"[FINE-TUNING START]")
        print(f"Dataset: {self.input_file}")
        print(f"Baseline cost: {self.baseline_cost}")
        print(f"Parameter sets to test: {self.num_parameter_sets}")
        print(f"Trials per parameter set: {Config.MIN_TRIALS}")
        print(f"CPU cores available: {cpu_count()}")
        
        for i in range(self.num_parameter_sets):
            params = generate_parameter_set(self.best_params)
            result = self.run_parameter_set(i + 1, params)
            self.results.append(result)
            
            # Update best parameters if this set performed better
            avg_cost = result['statistics']['average_cost']
            if avg_cost < self.best_avg_cost:
                self.best_avg_cost = avg_cost
                self.best_params = params.copy()
                print(f"  *** NEW BEST AVERAGE: {avg_cost:.2f} ***")
        
        self.export_results()
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print final summary of results."""
        print(f"\n{'='*80}")
        print(f"FINE-TUNING COMPLETE")
        print(f"{'='*80}")
        
        if self.results:
            best_result = min(self.results, key=lambda x: x['statistics']['best_cost'])
            best_avg_result = min(self.results, key=lambda x: x['statistics']['average_cost'])
            
            print(f"\nBest single result:")
            print(f"  Cost: {best_result['statistics']['best_cost']:.2f}")
            print(f"  Parameters: {best_result['parameters']}")
            
            print(f"\nBest average result:")
            print(f"  Average cost: {best_avg_result['statistics']['average_cost']:.2f} ± {best_avg_result['statistics']['std_deviation']:.2f}")
            print(f"  Parameters: {best_avg_result['parameters']}")
            
            if self.baseline_cost:
                best_gap = ((best_result['statistics']['best_cost'] - self.baseline_cost) / self.baseline_cost) * 100
                print(f"\nBaseline comparison:")
                print(f"  Baseline cost: {self.baseline_cost:.2f}")
                print(f"  Best gap: {best_gap:.1f}%")
