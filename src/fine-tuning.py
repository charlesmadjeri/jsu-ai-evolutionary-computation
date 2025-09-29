import argparse
import csv
import json
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path
from typing import Dict, List, Tuple, TypedDict, Union


class Config:
    ALGORITHM_TIMEOUT = 300  # 5 minutes
    DEFAULT_HIGH_COST = 10000.0
    
    EXPLOITATION_PROBABILITY = 0.7  # 70% chance to explore near best values
    EXPLORATION_VARIANCE = 0.15     # Gaussian variance for exploration
    
    PROGRESS_BAR_LENGTH = 40
    SEPARATOR_LENGTH = 70
    
    PARAM_RANGES = {
        'population_size': (10, 200),
        'elite_size_rate': (0.05, 0.5),
        'crossover_segment_rate': (0.1, 0.8),
        'stopping_generations': (50, 500),
        'stopping_improvement_rate': (0.0001, 0.01)
    }
    DEFAULT_PARAMS = {
        'population_size': 50,
        'elite_size_rate': 0.2,
        'crossover_segment_rate': 0.3,
        'stopping_generations': 200,
        'stopping_improvement_rate': 0.001
    }
    INTEGER_PARAMS = {'population_size', 'stopping_generations'}


class TuningResult(TypedDict):
    pass_num: int
    cost: float
    execution_time: float
    parameters: Dict[str, float]
    improvement: float


def parse_cost_from_output(output: str) -> float:
    for line in output.split('\n'):
        if 'cost' in line.lower() or 'distance' in line.lower():
            try:
                numbers = re.findall(r'[-+]?\d*\.?\d+', line)
                if numbers:
                    return float(numbers[-1])
            except (ValueError, IndexError):
                continue
    
    print("[!] Could not parse cost from output, using default high cost")
    return Config.DEFAULT_HIGH_COST


def build_algorithm_command(input_file: str, params: Dict[str, float]) -> List[str]:
    return [
        'python', 'main.py',
        '--input', input_file,
        '--export-image', 'true',
        '--export-csv', 'true',
        '--visualise', 'false',
        '--population-size', str(int(params['population_size'])),
        '--elite-size-rate', str(params['elite_size_rate']),
        '--crossover-segment-rate', str(params['crossover_segment_rate']),
        '--stopping-generations', str(int(params['stopping_generations'])),
        '--stopping-improvement-rate', str(params['stopping_improvement_rate'])
    ]


def execute_algorithm_worker(args: Tuple[int, str, Dict[str, float]]) -> TuningResult:
    pass_num, input_file, params = args
    cmd = build_algorithm_command(input_file, params)
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=Config.ALGORITHM_TIMEOUT
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode != 0:
            print(f"[!] Worker {pass_num}: Algorithm execution failed: {result.stderr}")
            cost = float('inf')
        else:
            cost = parse_cost_from_output(result.stdout)
            
    except subprocess.TimeoutExpired:
        print(f"[!] Worker {pass_num}: Algorithm execution timed out")
        cost = float('inf')
        execution_time = Config.ALGORITHM_TIMEOUT
    except Exception as e:
        print(f"[!] Worker {pass_num}: Error executing algorithm: {e}")
        cost = float('inf')
        execution_time = 0.0
    
    return {
        'pass_num': pass_num,
        'cost': cost,
        'execution_time': execution_time,
        'improvement': 0.0,
        'parameters': params.copy()
    }


class TSPTuner:
    def __init__(self, pass_number: int, input_file: str):
        self.pass_number = pass_number
        self.input_file = input_file
        self.results: List[TuningResult] = []
        self.best_params: Dict[str, float] = None
        self.best_cost = float('inf')
        self.current_params = Config.DEFAULT_PARAMS.copy()
    
    def generate_parameter_combination(self) -> Dict[str, float]:
        if self.best_params is None:
            return self.current_params.copy()
        
        new_params = {}
        
        for param, (min_val, max_val) in Config.PARAM_RANGES.items():
            if random.random() < Config.EXPLOITATION_PROBABILITY:
                best_val = self.best_params[param]
                range_size = max_val - min_val
                perturbation = random.gauss(0, range_size * Config.EXPLORATION_VARIANCE)
                new_val = best_val + perturbation
            else:
                new_val = random.uniform(min_val, max_val)
            
            new_val = max(min_val, min(max_val, new_val))
            
            if param in Config.INTEGER_PARAMS:
                new_val = int(round(new_val))
            
            new_params[param] = new_val
        
        return new_params
    
    def generate_parameter_combinations(self, num_combinations: int) -> List[Dict[str, float]]:
        combinations = []
        combinations.append(self.current_params.copy())
        
        for _ in range(num_combinations - 1):
            combinations.append(self.generate_parameter_combination())
        
        return combinations
    
    def calculate_improvement(self, current_cost: float, previous_cost: float) -> float:
        if previous_cost == 0:
            return 0.0
        return (previous_cost - current_cost) / previous_cost
    
    def display_status(self, current_pass: int, params: Dict[str, float], 
                      cost: float, exec_time: float, improvement: float):
        separator = "=" * Config.SEPARATOR_LENGTH
        
        print(f"\n{separator}")
        print(f">> PASS {current_pass}/{self.pass_number}")
        print(f"{separator}")
        
        print(f"\n[*] Current Parameters:")
        for param, value in params.items():
            if isinstance(value, float):
                print(f"   - {param:.<35} {value:.4f}")
            else:
                print(f"   - {param:.<35} {value}")
        
        print(f"\n[*] Results:")
        print(f"   - Cost: {cost:.2f}")
        print(f"   - Execution Time: {exec_time:.2f}s")
        print(f"   - Improvement: {improvement:+.2%}")
        
        print(f"\n[*] Best So Far:")
        print(f"   - Best Cost: {self.best_cost:.2f}")
        if self.best_params:
            print(f"   - Population Size: {self.best_params['population_size']}")
            print(f"   - Elite Size Rate: {self.best_params['elite_size_rate']:.3f}")
        
        progress = (current_pass / self.pass_number) * 100
        filled = int(Config.PROGRESS_BAR_LENGTH * current_pass / self.pass_number)
        bar = '#' * filled + '-' * (Config.PROGRESS_BAR_LENGTH - filled)
        print(f"\n[*] Progress: [{bar}] {progress:.1f}%")
        print(f"{separator}\n")
    
    def export_results(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path("results/tuning")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        json_file = results_dir / f"tuning_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'metadata': {
                    'total_passes': self.pass_number,
                    'input_file': self.input_file,
                    'timestamp': timestamp,
                    'best_cost': self.best_cost,
                    'best_params': self.best_params,
                    'cpu_cores_used': cpu_count()
                },
                'results': self.results
            }, f, indent=2)
        
        csv_file = results_dir / f"tuning_{timestamp}.csv"
        with open(csv_file, 'w', newline='') as f:
            if self.results:
                fieldnames = ['pass', 'cost', 'execution_time', 'improvement'] + \
                           list(self.results[0]['parameters'].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in self.results:
                    row: Dict[str, Union[int, float]] = {
                        'pass': result['pass_num'],
                        'cost': result['cost'],
                        'execution_time': result['execution_time'],
                        'improvement': result['improvement']
                    }
                    row.update(result['parameters'])
                    writer.writerow(row)
        
        print(f"\n[+] Results exported:")
        print(f"   - JSON: {json_file}")
        print(f"   - CSV:  {csv_file}")
    
    def display_final_results(self):
        separator = "=" * Config.SEPARATOR_LENGTH
        
        print(f"\n{separator}")
        print(f"[COMPLETE] PARALLEL TUNING COMPLETE")
        print(f"{separator}")
        print(f"\n[*] Final Best Results:")
        print(f"   - Best Cost: {self.best_cost:.2f}")
        print(f"\n   Best Parameters:")
        
        if self.best_params:
            for param, value in self.best_params.items():
                if isinstance(value, float):
                    print(f"   - {param:.<35} {value:.4f}")
                else:
                    print(f"   - {param:.<35} {value}")
        
        print(f"\n{separator}\n")
    
    def run(self):
        num_cores = cpu_count()
        
        print(f"\n[START] TSP Algorithm Tuner (PARALLEL)")
        print(f"   - Total Passes: {self.pass_number}")
        print(f"   - Input File: {self.input_file}")
        print(f"   - CPU Cores: {num_cores}")
        print(f"   - Passes per core: {self.pass_number // num_cores}")
        print(f"   - Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        all_results = []
        batch_size = max(1, num_cores)
        
        for batch_start in range(0, self.pass_number, batch_size):
            batch_end = min(batch_start + batch_size, self.pass_number)
            batch_passes = batch_end - batch_start
            
            print(f"\n[BATCH] Processing passes {batch_start + 1}-{batch_end}")
            
            param_combinations = self.generate_parameter_combinations(batch_passes)

            worker_args = []
            for i, params in enumerate(param_combinations):
                pass_num = batch_start + i + 1
                worker_args.append((pass_num, self.input_file, params))
            
            with ProcessPoolExecutor(max_workers=num_cores) as executor:
                batch_results = list(executor.map(execute_algorithm_worker, worker_args))
            
            for result in batch_results:
                if all_results:
                    last_cost = all_results[-1]['cost']
                    improvement = self.calculate_improvement(result['cost'], last_cost)
                else:
                    improvement = 0.0
                
                result['improvement'] = improvement
                
                if result['cost'] < self.best_cost:
                    self.best_cost = result['cost']
                    self.best_params = result['parameters'].copy()
                
                all_results.append(result)
                self.display_status(result['pass_num'], result['parameters'], 
                                  result['cost'], result['execution_time'], improvement)
        
        self.results = sorted(all_results, key=lambda x: x['pass_num'])
        self.export_results()
        self.display_final_results()


def validate_arguments(args) -> None:
    if args.pass_number <= 0:
        print("[X] Error: pass_number must be greater than 0")
        sys.exit(1)
    
    if not Path(args.input).exists():
        print(f"[X] Error: Input file not found: {args.input}")
        sys.exit(1)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='TSP Algorithm Parameter Tuner - Parallel Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage: 
    python fine-tuning.py <pass_number> -i <input_file>
        """
    )
    parser.add_argument(
        'pass_number',
        type=int,
        help='Number of tuning passes to execute'
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to input CSV file with city coordinates'
    )
    
    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    
    validate_arguments(args)
    
    tuner = TSPTuner(args.pass_number, args.input)
    tuner.run()


if __name__ == "__main__":
    main()