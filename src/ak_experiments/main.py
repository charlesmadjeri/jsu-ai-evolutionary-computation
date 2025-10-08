import sys
import os

print(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from datetime import datetime
from argparse import ArgumentParser
from csv import reader as csv_reader
from math import inf
from multiprocessing import Process, Queue, cpu_count
from threading import Thread
import time

from typing import TypedDict

from stop_criterions.time_stop_criterion import TimeStopCriterion
from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from cost_calculation.euclidean_cost_calculation import EuclideanCostCalculation
from crossover.order_crossover import OrderCrossover
from crossover.partially_mapped_crossover import PartiallyMappedCrossover
from elite_selector.elite_selector import EliteSelector
from load_csv import load_csv
from solvers.callbacks.evolutionary_callback import EvolutionaryCallback
from solvers.evolutionary_solver import EvolutionarySolver

results_dir = os.path.join(os.path.dirname(__file__), "results")

THRESHOLD_TIME_PERCENTAGE = 70.

class DatasetData():
    def __init__(self, name: str, res_path: str, data: list[tuple[float, float]], gf_cost: float, gf_time: float, threshold_percentage: float):
        self.name = name
        self.res_path = res_path
        self.data = data
        self.gf_cost = gf_cost
        self.gf_time = gf_time
        self.threshold_time = gf_time * THRESHOLD_TIME_PERCENTAGE
        self.threshold_percentage = threshold_percentage
        self.best_cost = inf
        # File header is created in main
    
    def create_file_header(self):
        """Create the CSV file header - called once from main process"""
        generations_str = ",".join([f"{i}gen_iteration,{i}gen_cost,{i}gen_elapsed_time" for i in range(1, 20)])
        with open(self.res_path, "w") as f:
            f.write(f"elite_size,cost_calculator,population_size,crossover_type,segment_length,best_cost,elapsed_time,{generations_str}\n")

class ThreadData(TypedDict):
    ea: EvolutionarySolver
    dataset: DatasetData

class NewBestSolutionInfo(TypedDict):
    elapsed_time: float
    cost: float
    iteration: int    
        
class EACallable(EvolutionaryCallback):
    def __init__(self):
        self.best_cost = inf
        self.best_generations: list[NewBestSolutionInfo] = []
        self.elite_iteration = 0

    def on_start(self, dataset: list[tuple[float, float]], starting_generation: list[list[int]]):
        self.start_time = time.time()

    def on_new_elites(self, elites: list[tuple[list[int], float]]):
        self.elite_iteration += 1
        elite_best = elites[0]
        if self.best_cost > elite_best[1]:
            self.best_cost = elite_best[1]
            self.best_generations.append({
                "elapsed_time": time.time() - self.start_time,
                "cost": elite_best[1],
                "iteration": self.elite_iteration
            })

    def on_end(self, order: list[int], cost: float):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        self.best_cost = cost

def ea_to_string(ea: EvolutionarySolver):
    if isinstance(ea.crossover, OrderCrossover):
        crossover_type = "ordered"
    elif isinstance(ea.crossover, PartiallyMappedCrossover):
        crossover_type = "partially-mapped"
    else:
        crossover_type = "unknown"
    
    if ea.crossover.segment_length is None:
        segment_length = "random"
    else:
        segment_length = ea.crossover.segment_length
    
    if ea.elite_selector.cost_calculator == ManhattanCostCalculation:
        cost_calculator = "manhattan"
    elif ea.elite_selector.cost_calculator == EuclideanCostCalculation:
        cost_calculator = "euclidean"
    else:
        cost_calculator = "unknown"
    
    return f"{ea.elite_selector.elite_size},{cost_calculator},{ea.population_size},{crossover_type},{segment_length}"

def worker_function(work_queue: Queue, result_queue: Queue):
    """Worker process that processes EA tasks from the work queue."""
    while True:
        task = work_queue.get()  # Blocks until work is available
        if task is None:  # Poison pill to stop
            break
            
        # Unpack configuration and create EA solver in worker process
        # This avoids pickling the crossover objects with their lambda functions
        config = task["config"]
        dataset_data = task["dataset"]
        
        # Create the EA solver with the provided configuration
        ea = EvolutionarySolver(
            elite_selector=EliteSelector(config["cost_calculator"], elite_size=config["elite_size"]),
            crossover=config["crossover_type"](config["segment_length"]),
            stop_criterions=[TimeStopCriterion(config["threshold_seconds"])],
            population_size=config["population_size"],
            minimum_iterations=config["minimum_iterations"]
        )
        
        callable = EACallable()
        ea.callbacks = [callable]
        _, res = ea.solve(dataset_data.data)
        
        # Send result back to main process
        result_queue.put({
            "dataset_name": dataset_data.name,
            "res_path": dataset_data.res_path,
            "threshold_percentage": dataset_data.threshold_percentage,
            "threshold_time": dataset_data.threshold_time,
            "gf_cost": dataset_data.gf_cost,
            "gf_time": dataset_data.gf_time,
            "cost": res,
            "elapsed_time": callable.elapsed_time,
            "ea_string": ea_to_string(ea),
            "best_generations": callable.best_generations
        })

def result_handler(result_queue: Queue, dataset_best_costs: dict, stop_flag: list):
    """Thread that handles results as they come in."""
    results_collected = 0
    while True:
        try:
            result = result_queue.get(timeout=0.1)
        except:
            # Check if we should stop
            if stop_flag[0]:
                break
            continue
        
        results_collected += 1
        dataset_name = result["dataset_name"]
        
        # Filter generations that took too long
        best_generations = [g for g in result["best_generations"] if g['elapsed_time'] <= result["threshold_time"]]

        if len(best_generations) == 0:
            continue
        
        is_best = dataset_name not in dataset_best_costs or dataset_best_costs[dataset_name] > result["cost"]
        if is_best:
            dataset_best_costs[dataset_name] = result["cost"]
            print(f"New best cost={result['cost']} ({result['gf_cost'] / result['cost'] * 100:.2f}% of greedy result) "
                  f"time={result['elapsed_time']:.4f}s (gf_time={result['gf_time']:.4f}s "
                  f"t_increase={result['elapsed_time']/result['gf_time'] * 100 - 100.:.2f}%) "
                  f"for {result['ea_string']}")

        save_to_file = is_best or result["cost"] <= result["threshold_percentage"] * dataset_best_costs[dataset_name]
        if save_to_file:
            generations_str = ",".join([f"{g['iteration']},{g['cost']},{g['elapsed_time']}" for g in best_generations])
            with open(result["res_path"], "a") as f:
                f.write(f"{result['ea_string']},{result['cost']},{result['elapsed_time']},{generations_str}\n")
        
    
    print(f"Result handler collected {results_collected} results.")

def load_datasets_info(dir: str, info_path: str):
    result = {}
    with open(os.path.join(dir, info_path), "r") as file:
        reader = csv_reader(file)
        header_skipped = False
        for row in reader:
            if not header_skipped:
                header_skipped = True
                continue
            
            try:
                cost = float(row[2])
            except ValueError:
                cost = int(row[2])
            result[row[0]] = {
                "length": int(row[1]),
                "gf-cost": cost,
                "gf-time": float(row[3]),
            }
    return result

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-k", "--keys", dest="dataset_keys", type=str, nargs="*", default=["eil76", "pr136", "a280"])
    parser.add_argument("-t", "--thread-percentage", dest="thread_percentage", type=float, default=0.9)
    parser.add_argument("-tc", "--threshold-cost", dest="threshold_cost", type=float, default=1.05)
    parser.add_argument("-min_it", "--minimum", dest="min_it", type=int, default=25)
    parser.add_argument("-dir", "--directory", dest="dir", type=str, default="data/TSPLIB/export")
    parser.add_argument("-if", "--info-file", dest="info_file", type=str, default="_file_lengths.csv")
    parser.add_argument("-i", "--iterations", dest="parameters_set_repeat", type=int, default=1)
    args = parser.parse_args()
    print(args)
    if not args.info_file.endswith(".csv"):
        args.info_file += ".csv"

    assert args.threshold_cost > 0.9999999

    args.parameters_set_repeat = max(1, args.parameters_set_repeat)

    datasets_info = load_datasets_info(args.dir, args.info_file)

    if not isinstance(args.dataset_keys, list):
        args.dataset_keys = [args.dataset_keys]

    for k in args.dataset_keys:
        if k.endswith(".csv"):
            k = k.replace(".csv", "")
        if k.endswith(".tsp"):
            k = k.replace(".tsp", "")
        assert k in datasets_info.keys(), f"Dataset {k} not found in {args.info_file}"

    cpu_c = cpu_count() - 1  # -1 => main process is also used
    cpu_c = int(max(1, min(args.thread_percentage * cpu_c, cpu_c)))
    print(f"Running {cpu_c} worker processes")

    os.makedirs(results_dir, exist_ok=True)
    
    # Create work and result queues
    work_queue = Queue()
    result_queue = Queue()
    
    # Track best costs per dataset
    dataset_best_costs = {}
    
    # Start result handler thread
    stop_flag = [False]
    result_thread = Thread(target=result_handler, args=(result_queue, dataset_best_costs, stop_flag))
    result_thread.start()
    
    # Start worker processes
    processes = []
    for i in range(cpu_c):
        p = Process(target=worker_function, args=(work_queue, result_queue))
        p.start()
        processes.append(p)

    max_queue_size = cpu_c * 2
    for i in range(args.parameters_set_repeat):
        print(f"Running parameters set {i+1}/{args.parameters_set_repeat}")
        for crossover_type in [PartiallyMappedCrossover, OrderCrossover]: # FIXME: update to whatever is needed
            for k in args.dataset_keys:
                current_info = datasets_info[k]
                dataset_data = DatasetData(name=k, res_path=os.path.join(results_dir, f"{k} {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.csv"), data=load_csv(os.path.join(args.dir, k + ".csv")), gf_cost=current_info['gf-cost'], gf_time=current_info['gf-time'], threshold_percentage=args.threshold_cost)
                dataset_data.create_file_header()
                threshold_seconds = dataset_data.threshold_time
                print(f"Running {k} dataset, greedy first with {current_info['length']} cities to beat: cost={current_info['gf-cost']:.2f} time={current_info['gf-time']:.4f}s, threshold: percentage={dataset_data.threshold_percentage * 100.:.2f}% time={threshold_seconds:.4f}s")
                assert len(dataset_data.data) == current_info["length"]
                if current_info["length"] < 3:
                    continue
                previous_population_size = -1
                
                for cost_calculator in [ManhattanCostCalculation]: # FIXME: update to whatever is needed
                    for population_size in range(25, 3010, 25): # FIXME: update to whatever is needed
                    # for __population_size in range(3, 101, 1): # FIXME: update to whatever is needed
                    #     population_size = int(max(3, current_info["length"] * __population_size / 100.))
                    #     if population_size == previous_population_size:
                    #         continue
                        print(f"Starting population size={population_size} ({population_size/current_info['length']*100:.2f}%)")
                        # previous_population_size = population_size
                        previous_elite_size = -1
                        for __elite_size in range(1, 20, 1): # FIXME: update to whatever is needed
                            elite_size = max(2, min(int(population_size * __elite_size / 100.), population_size-1))
                            if elite_size == previous_elite_size:
                                continue
                            previous_elite_size = elite_size
                            previous_segment_length = -1
                            
                            # Submit task with None segment_length
                            work_queue.put({
                                "config": {
                                    "cost_calculator": cost_calculator,
                                    "elite_size": elite_size,
                                    "crossover_type": crossover_type,
                                    "segment_length": None,
                                    "threshold_seconds": threshold_seconds,
                                    "population_size": population_size,
                                    "minimum_iterations": args.min_it
                                },
                                "dataset": dataset_data
                            })
                            
                            for __segment_length in range(1, 40, 1): # FIXME: update to whatever is needed
                                segment_length = max(1, min(int(current_info["length"] * __segment_length / 100.), current_info["length"]-1))
                                if segment_length == previous_segment_length:
                                    continue
                                previous_segment_length = segment_length
                                
                                # Submit task with specific segment_length
                                work_queue.put({
                                    "config": {
                                        "cost_calculator": cost_calculator,
                                        "elite_size": elite_size,
                                        "crossover_type": crossover_type,
                                        "segment_length": segment_length,
                                        "threshold_seconds": threshold_seconds,
                                        "population_size": population_size,
                                        "minimum_iterations": args.min_it
                                    },
                                    "dataset": dataset_data
                                })

    # Send poison pills to stop workers
    print("All work submitted, waiting for worker processes to finish...")
    for _ in range(cpu_c):
        work_queue.put(None)
    
    # Wait for all workers to finish
    for process in processes:
        process.join()
    
    # Give result handler time to process remaining results
    time.sleep(0.5)
    
    # Stop result handler thread
    stop_flag[0] = True
    result_thread.join()
    
    print(f"All {cpu_c} worker processes finished!")