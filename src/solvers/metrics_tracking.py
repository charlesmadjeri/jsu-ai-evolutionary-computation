class MeticTracker:
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
            k:sum(v) if all(isinstance(i, (int, float)) for i in v) else v
            for k, v in self.metrics.items()
        }
    
    def reset(self):
        self.metrics.clear() 