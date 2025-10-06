from pprint import pprint
from solvers.callbacks.greedy_first_callback import GreedyFirstCallback

class MetricTracker(GreedyFirstCallback):
    i = 1

    def __init__(self):
        super().__init__()
        self.metrics = {}
        self.local_i = MetricTracker.i
        MetricTracker.i += 1

    def on_start(self, dataset: list[tuple[float, float]], starting_node: int):
        self.log("start_node", starting_node)
    
    def on_iteration(self, processing_node: int):
        self.log("greedy_step", 1)
    
    def on_cost_calculation(self, node_a: int, node_b: int, result: float):
        self.log("distance_calculations", 1)
    
    def on_end(self, order: list[int], cost: float):
        self.log("final_distance", cost)
        print(f"\n--- Metrics for run {self.local_i} ---")
        metrics = self.summary()
        pprint(metrics)
        print("------------------------\n")

    def log(self, name, value):
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def get(self, name):
        return self.metrics.get(name, [])
    
    def summary(self):
        return {
            metric_name: sum(metric_values) if all(isinstance(item, (int, float)) for item in metric_values) else metric_values
            for metric_name, metric_values in self.metrics.items()
        }
    
    def reset(self):
        self.metrics.clear()