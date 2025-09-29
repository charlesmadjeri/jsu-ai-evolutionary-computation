from typing import Dict, List, Union, TypedDict

class TrialResult(TypedDict):
    """Result of a single trial test"""
    trial_id: int
    best_cost: float
    execution_time: float
    total_iterations: int
    convergence_data: List[Dict]
    parameters: Dict[str, Union[int, float]]

class ParameterSetResult(TypedDict):
    """Result of a full parameter set test"""
    parameters: Dict[str, Union[int, float]]
    trials: List[TrialResult]
    statistics: Dict[str, float]
    baseline_comparison: Dict[str, float]
