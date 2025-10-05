from typing import Callable, Optional

Point = tuple[float, float]
CostCalculationCallback = Callable[[Point, Point, float], None]

class GreedyFirstCallback():
    def __init__(
        self, 
        on_start: Optional[Callable[[int], None]] = None,
        on_iteration: Optional[Callable[[int], None]] = None,
        on_end: Optional[Callable[[float], None]] = None,
        on_cost_calculation: Optional[CostCalculationCallback] = None
    ):
        self.on_start = on_start or (lambda starting_node: None)
        self.on_iteration = on_iteration or (lambda iteration: None)
        self.on_end = on_end or (lambda result: None)
        self.on_cost_calculation = on_cost_calculation or (lambda pt_a, pt_b, cost: None)