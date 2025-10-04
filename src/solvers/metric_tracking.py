class MetricTracker:
    def __init__(self):
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