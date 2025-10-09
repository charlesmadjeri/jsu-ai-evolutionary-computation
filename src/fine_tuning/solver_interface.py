import json
import subprocess
import time
from typing import Dict, List, Tuple, Union

from .config import Config
from .types import TrialResult

def parse_solver_output(output: str) -> Dict:
    result = {
        'best_cost': None,
        'execution_time': None,
        'total_iterations': None,
        'convergence_data': []
    }
    
    lines = output.split('\n')
    in_final_result = False
    
    for line in lines:
        line = line.strip()
        
        if line == "FINAL_RESULT_START":
            in_final_result = True
            continue
        elif line == "FINAL_RESULT_END":
            in_final_result = False
            continue
        
        if in_final_result:
            if line.startswith("BEST_COST:"):
                try:
                    result['best_cost'] = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("EXECUTION_TIME:"):
                try:
                    result['execution_time'] = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("TOTAL_ITERATIONS:"):
                try:
                    result['total_iterations'] = int(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("CONVERGENCE_DATA:"):
                try:
                    json_str = line.split(":", 1)[1].strip()
                    result['convergence_data'] = json.loads(json_str)
                except:
                    pass
    
    return result

def build_solver_command(input_file: str, params: Dict[str, Union[int, float]]) -> List[str]:
    cmd = [
        'python3', 'src/main.py',
        '-ps', str(int(params['population_size']) if isinstance(params['population_size'], (int, float)) else params['population_size']),
        '-es', str(params['elite_size']),
        '-cr', 'order',
        '-cs', str(params['crossover_segment']),
        '-sit', str(int(params['stop_iterations'])),
        '-sim', str(params['stop_improvement']),
        '-cc', 'manhattan',
        '--verbose', '1',
        input_file
    ]
    return cmd

def run_single_trial(args: Tuple[int, str, Dict[str, Union[int, float]]]) -> TrialResult:
    trial_id, input_file, params = args
    cmd = build_solver_command(input_file, params)
    
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=Config.ALGORITHM_TIMEOUT
        )
        
        if result.returncode != 0:
            print(f"[ERROR] Trial {trial_id} failed: {result.stderr}")
            return {
                'trial_id': trial_id,
                'best_cost': float('inf'),
                'execution_time': time.time() - start_time,
                'total_iterations': 0,
                'convergence_data': [],
                'parameters': params.copy()
            }
        
        parsed = parse_solver_output(result.stdout)
        
        return {
            'trial_id': trial_id,
            'best_cost': parsed['best_cost'] if parsed['best_cost'] is not None else float('inf'),
            'execution_time': parsed['execution_time'] if parsed['execution_time'] is not None else time.time() - start_time,
            'total_iterations': parsed['total_iterations'] if parsed['total_iterations'] is not None else 0,
            'convergence_data': parsed['convergence_data'],
            'parameters': params.copy()
        }
        
    except subprocess.TimeoutExpired:
        print(f"[WARNING] Trial {trial_id} timed out")
        return {
            'trial_id': trial_id,
            'best_cost': float('inf'),
            'execution_time': Config.ALGORITHM_TIMEOUT,
            'total_iterations': 0,
            'convergence_data': [],
            'parameters': params.copy()
        }
    except Exception as e:
        print(f"[ERROR] Trial {trial_id} failed with exception: {e}")
        return {
            'trial_id': trial_id,
            'best_cost': float('inf'),
            'execution_time': time.time() - start_time,
            'total_iterations': 0,
            'convergence_data': [],
            'parameters': params.copy()
        }
