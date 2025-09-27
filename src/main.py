#!/usr/bin/env python3
"""
Jonkoping School of Engineering (JTH)
Data Analysis Project

Team Members:
- Aikeya Ainiwaer
- Andrej Kutny
- Charles Madjeri
- Samrat Debnath
- Vladimir Giustacchini

AI course - Evolutionary computation assignment
"""

from ast import arg
import sys
import os
from typing import Optional

from export import generate_png_export
from utils.arg_parser import main_parser

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main() -> int:
    args = main_parser()
    exit(0)

    from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
    # from cost_calculation.euclidean_cost_calculation import EuclideanCostCalculation
    from solvers.greedy_first import GreedyFirst
    from utils.tsp_kaggle_convert import load_tsp_kaggle_data
    import time
    from export import generate_png_export

    from random import sample
    
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    os.makedirs(save_dir, exist_ok=True)
    
    greedy_first = GreedyFirst(ManhattanCostCalculation())
    for i in sample(range(300), 10):
        input_data = load_tsp_kaggle_data(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "dataset.csv"), i)
        start = time.time()
        result, distance = greedy_first.solve(input_data)
        end = time.time()
        img = generate_png_export.generate_png_export(result)
        
        generate_png_export.save_map(img, os.path.join(save_dir, f"result_{i}.png") )
        print(f"{i} of size {len(input_data)} solved in {end - start} seconds, total distance is {distance}")
        assert len(result) == len(input_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())