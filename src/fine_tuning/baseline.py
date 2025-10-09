import re
from pathlib import Path
from typing import Optional

def load_baseline_result(dataset_name: str) -> Optional[float]:
    baseline_file = Path(f"results/baseline/{dataset_name}")
    if not baseline_file.exists():
        print(f"[WARNING] Baseline file not found: {baseline_file}")
        return None
    
    try:
        with open(baseline_file, 'r') as f:
            content = f.read()
            match = re.search(r'TOTAL_DISTANCE_CALCULATED:\s*([0-9.]+)', content)
            if match:
                return float(match.group(1))
            else:
                print(f"[WARNING] Could not parse baseline distance from {baseline_file}")
                return None
    except Exception as e:
        print(f"[ERROR] Failed to load baseline from {baseline_file}: {e}")
        return None
