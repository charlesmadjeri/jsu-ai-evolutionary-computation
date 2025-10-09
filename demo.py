import subprocess
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from typing import Dict, List, Tuple
import time

FINE_TUNED_PARAMS = {
    'population_size': 2000,
    'elite_size': 0.046,
    'crossover_segment': 0.27,
    'stop_iterations':67,
    'stop_improvement': 0.00070
}

def run_baseline_algorithm(dataset_path: str) -> Tuple[float, List[Dict]]:
    print("Running baseline algorithm (greedy-first)...")
    
    cmd = [
        '/usr/bin/python3', 'src/main.py', 
        dataset_path, 
        '-gf',
        '--verbose', '1'
    ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode != 0:
        print(f"Baseline algorithm failed: {result.stderr}")
        return float('inf'), []
    
    baseline_cost = float('inf')
    convergence_data = []
    
    lines = result.stdout.split('\n')
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
                    baseline_cost = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("CONVERGENCE_DATA:"):
                try:
                    json_str = line.split(":", 1)[1].strip()
                    convergence_data = json.loads(json_str)
                except:
                    pass
        else:
            if line.startswith("Distance:"):
                try:
                    baseline_cost = float(line.split(":", 1)[1].strip())
                except:
                    pass
    
    print(f"Baseline cost: {baseline_cost:.2f}")
    return baseline_cost, convergence_data

def run_fine_tuned_algorithm(dataset_path: str, run_id: int) -> Tuple[float, List[Dict]]:
    print(f"Running fine-tuned algorithm (run {run_id}/5)...")
    
    cmd = [
        '/usr/bin/python3', 'src/main.py',
        dataset_path,
        '-ps', str(FINE_TUNED_PARAMS['population_size']),
        '-es', str(FINE_TUNED_PARAMS['elite_size']),
        '-cs', str(FINE_TUNED_PARAMS['crossover_segment']),
        '-sit', str(FINE_TUNED_PARAMS['stop_iterations']),
        '-sim', str(FINE_TUNED_PARAMS['stop_improvement']),
        '--verbose', '1'
    ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode != 0:
        print(f"Fine-tuned algorithm run {run_id} failed: {result.stderr}")
        return float('inf'), []
    
    best_cost = float('inf')
    convergence_data = []
    
    lines = result.stdout.split('\n')
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
                    best_cost = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("CONVERGENCE_DATA:"):
                try:
                    json_str = line.split(":", 1)[1].strip()
                    convergence_data = json.loads(json_str)
                except:
                    pass
    
    print(f"Fine-tuned run {run_id} cost: {best_cost:.2f}")
    return best_cost, convergence_data

def create_visualization(baseline_cost: float, baseline_convergence: List[Dict], 
                        fine_tuned_results: List[Tuple[float, List[Dict]]]):    
    plt.figure(figsize=(12, 8))
    
    if baseline_convergence:
        baseline_iterations = [d['iteration'] for d in baseline_convergence]
        baseline_costs = [d['best_cost'] for d in baseline_convergence]
        plt.plot(baseline_iterations, baseline_costs, 'r-', linewidth=2, 
                label=f'Baseline (Greedy-First): {baseline_cost:.2f}', alpha=0.8)
    
    colors = ['blue', 'green', 'orange', 'purple', 'brown']
    for i, (cost, convergence_data) in enumerate(fine_tuned_results):
        if convergence_data:
            iterations = [d['iteration'] for d in convergence_data]
            costs = [d['best_cost'] for d in convergence_data]
            plt.plot(iterations, costs, color=colors[i % len(colors)], 
                    linewidth=1.5, alpha=0.7, 
                    label=f'Fine-tuned Run {i+1}: {cost:.2f}')
    
    plt.xlabel('Iteration')
    plt.ylabel('Best Cost')
    plt.title('TSP Algorithm Cost Evolution: Baseline vs Fine-tuned')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if not baseline_convergence:
        plt.axhline(y=baseline_cost, color='red', linestyle='--', linewidth=2, 
                   label=f'Baseline (Greedy-First): {baseline_cost:.2f}')
        plt.legend()
    
    plt.tight_layout()
    
    output_path = 'demo_cost_evolution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved as: {output_path}")
    
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage: python demo.py <dataset_path>")
        print("Example: python demo.py data/vm1084.csv")
        sys.exit(1)
    
    dataset_path = sys.argv[1]
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found.")
        sys.exit(1)
    
    print("=" * 60)
    print("TSP Algorithm Demo: Baseline vs Fine-tuned")
    print("=" * 60)
    print(f"Dataset: {dataset_path}")
    print(f"Fine-tuned parameters: {FINE_TUNED_PARAMS}")
    print()
    
    baseline_cost, baseline_convergence = run_baseline_algorithm(dataset_path)
    print()
    
    fine_tuned_results = []
    for i in range(5):
        cost, convergence = run_fine_tuned_algorithm(dataset_path, i + 1)
        fine_tuned_results.append((cost, convergence))
        print()
    
    fine_tuned_costs = [result[0] for result in fine_tuned_results]
    valid_costs = [cost for cost in fine_tuned_costs if cost != float('inf')]
    
    if valid_costs:
        avg_fine_tuned = np.mean(valid_costs)
        std_fine_tuned = np.std(valid_costs)
        best_fine_tuned = min(valid_costs)
        
        print("=" * 60)
        print("RESULTS SUMMARY")
        print("=" * 60)
        print(f"Baseline (Greedy-First): {baseline_cost:.2f}")
        print(f"Fine-tuned - Best: {best_fine_tuned:.2f}")
        print(f"Fine-tuned - Average: {avg_fine_tuned:.2f} ± {std_fine_tuned:.2f}")
        print(f"Improvement: {((baseline_cost - best_fine_tuned) / baseline_cost * 100):.1f}%")
        print()
    
    print("Creating visualization...")
    create_visualization(baseline_cost, baseline_convergence, fine_tuned_results)
    
    print("Demo completed!")

if __name__ == "__main__":
    main()
