from solvers.callbacks.greedy_first_callback import GreedyFirstCallback

class MetricTracker(GreedyFirstCallback):
    def __init__(self):
        super().__init__(
            on_start = lambda start_node: self.metric_tracker.log("start_node", start_node), 
            on_iteration = lambda _: self.metric_tracker.log("greedy_step", 1), 
            on_cost_calculation = lambda pt_a, pt_b, cost: self.metric_tracker.log("distance_calculations", 1),
            on_end = lambda total_distance: self.metric_tracker.log("final_distance", total_distance)
        )
        self.metrics = {}
    
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