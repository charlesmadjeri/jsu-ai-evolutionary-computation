from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from solvers.callbacks.metric_tracking import MetricTracker
from solvers.greedy_first import GreedyFirst

def test_metric_tracking():
    dataset = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    metric_tracker1 = MetricTracker()
    metric_tracker2 = MetricTracker()
    gf1 = GreedyFirst(ManhattanCostCalculation, callbacks=[metric_tracker1, metric_tracker2])
    gf1.solve(dataset)
    metric_tracker3 = MetricTracker()
    gf2 = GreedyFirst(ManhattanCostCalculation, callbacks=[metric_tracker3])
    gf2.solve(dataset)
    assert metric_tracker1.metrics == metric_tracker2.metrics == metric_tracker3.metrics
    assert MetricTracker.i == 4 == metric_tracker1.i == metric_tracker2.i == metric_tracker3.i
    assert metric_tracker1.local_i != metric_tracker2.local_i != metric_tracker3.local_i