class Config:
    ALGORITHM_TIMEOUT = 300  # 5 minutes per run
    DEFAULT_HIGH_COST = 10000000000.0
    MIN_TRIALS = 25
    
    # Exploration vs exploitation balance
    EXPLOITATION_PROBABILITY = 0.7  # 70% chance to explore near best values
    EXPLORATION_VARIANCE = 0.15     # Gaussian variance for exploration
    
    # Parameter tuning ranges for evolutionary algorithm
    PARAM_RANGES = {
        'population_size': (100, 3000),
        'elite_size': (0.01, 0.1),
        'crossover_segment': (0.1, 0.3),
        'stop_iterations': (25, 200),
        'stop_improvement': (0.0001, 0.001)
    }
    
    # Default parameters as starting point
    DEFAULT_PARAMS = {
        'population_size': 1599,
        'elite_size': 0.05,
        'crossover_segment': 0.12,
        'stop_iterations': 100,
        'stop_improvement': 0.00075
    }
    
    INTEGER_PARAMS = {'population_size', 'stop_iterations'}
