import random
from typing import Dict, Optional, Union

from .config import Config

def generate_parameter_set(best_params: Optional[Dict] = None) -> Dict[str, Union[int, float]]:
    if best_params is None:
        params = Config.DEFAULT_PARAMS.copy()
    else:
        params = {}
        for param, (min_val, max_val) in Config.PARAM_RANGES.items():
            if random.random() < Config.EXPLOITATION_PROBABILITY:
                best_val = best_params[param]
                range_size = max_val - min_val
                perturbation = random.gauss(0, range_size * Config.EXPLORATION_VARIANCE)
                new_val = best_val + perturbation
            else:
                new_val = random.uniform(min_val, max_val)
            
            new_val = max(min_val, min(max_val, new_val))
            
            if param in Config.INTEGER_PARAMS:
                new_val = int(round(new_val))
            
            params[param] = new_val
    
    return params
