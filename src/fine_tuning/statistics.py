import statistics
from typing import Dict, List, Optional

from .types import TrialResult

def calculate_statistics(trials: List[TrialResult], baseline_cost: Optional[float] = None) -> Dict:
    valid_costs = [t['best_cost'] for t in trials if t['best_cost'] != float('inf')]
    
    if not valid_costs:
        return {
            'best_cost': float('inf'),
            'average_cost': float('inf'),
            'std_deviation': float('inf'),
            'average_execution_time': 0.0,
            'success_rate': 0.0,
            'baseline_gap_percent': float('inf') if baseline_cost else None
        }
    
    statistics_dict = {
        'best_cost': min(valid_costs),
        'average_cost': statistics.mean(valid_costs),
        'std_deviation': statistics.stdev(valid_costs) if len(valid_costs) > 1 else 0.0,
        'average_execution_time': statistics.mean([t['execution_time'] for t in trials]),
        'success_rate': len(valid_costs) / len(trials)
    }
    
    if baseline_cost:
        best_gap = ((statistics_dict['best_cost'] - baseline_cost) / baseline_cost) * 100
        avg_gap = ((statistics_dict['average_cost'] - baseline_cost) / baseline_cost) * 100
        statistics_dict.update({
            'baseline_gap_best_percent': best_gap,
            'baseline_gap_average_percent': avg_gap
        })
    
    return statistics_dict
