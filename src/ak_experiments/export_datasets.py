import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from argparse import ArgumentParser
from os import listdir
from os.path import join
from time import time
from dataparser.dot_tsp_parser import load_tsp_data
from solvers.greedy_first import GreedyFirst
from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-gf", dest="use_greedy_first", action="store_true", default=False)
    parser.add_argument("-w", "--whitelist", dest="whitelist", type=str, nargs="*", default=[])
    parser.add_argument("-dir", dest="dir", type=str, default="data/TSPLIB")
    args = parser.parse_args()

    if not isinstance(args.whitelist, list):
        args.whitelist = [args.whitelist]

    BASE_DIR = args.dir
    EXPORT_DIR = join(BASE_DIR, "export")
    FILE_LENGTHS_FILE = join(EXPORT_DIR, "_file_lengths.csv")
    os.makedirs(EXPORT_DIR, exist_ok=True)

    with open(FILE_LENGTHS_FILE, "w") as f:
        f.write(f"file,length{',gf-cost,gf-time,gf-order' if args.use_greedy_first else ''}\n")

    for file in listdir(BASE_DIR):
        if not file.endswith(".tsp"):
            continue
        stripped_filename = file.replace(".tsp", "")
        if args.whitelist and stripped_filename not in args.whitelist:
            continue
        data = load_tsp_data(join(BASE_DIR, file))
        with open(join(EXPORT_DIR, stripped_filename + ".csv"), "w") as f:
            f.write(f"x,y\n")
            for x, y in data:
                f.write(f"{x},{y}\n")
        gf_str = ""
        if args.use_greedy_first:
            gf = GreedyFirst(cost_calculator=ManhattanCostCalculation)
            elapsed = time()
            try:
                order, cost = gf.solve(data)
            except Exception as e:
                print(f"Error solving {file}: {e}")
                continue
            elapsed = time() - elapsed
            gf_str = f",{cost},{elapsed},\"{order}\""
            print(f"{stripped_filename} done in {elapsed:.6f}s with cost {cost:.2f}")
        length = len(data)
        with open(FILE_LENGTHS_FILE, "a") as f:
            f.write(f"{stripped_filename},{length}{gf_str}\n")
