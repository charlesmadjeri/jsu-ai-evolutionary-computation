import sys
import os

print(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from datetime import datetime
from argparse import ArgumentParser
from csv import reader as csv_reader
from math import inf
from multiprocessing import Lock
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

class DatasetData():
    def __init__(self, name: str, res_path: str, data: list[tuple[float, float]], gf_cost: float, gf_time: float, threshold_percentage: float):
        self.name = name
        self.res_path = res_path
        self.data = data
        self.gf_cost = gf_cost
        self.gf_time = gf_time
        self.threshold_cost = gf_cost * (2. - threshold_percentage)
        self.best_cost = inf
        self.res_lock = Lock()
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

is_active = True
ea_list: list[ThreadData] = []

ea_data_lock = Lock()
        
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

    def save(self, dataset_info: str, csv_path: str):
        generations_str = ",".join([f"{generation['iteration']},{generation['cost']},{generation['elapsed_time']}" for generation in self.best_generations])
        with open(csv_path, "a") as f:
            f.write(f"{dataset_info},{self.best_cost},{self.elapsed_time},{generations_str}\n")

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

def worker_function():
    while True:
        ea_data_lock.acquire()
        if len(ea_list) == 0:
            ea_data_lock.release()
            if not is_active:
                break
            time.sleep(0.025) # sleep for 25ms TODO: better approach? Use conditional variable?
            continue
        ea_data = ea_list.pop(0)
        ea_data_lock.release()
        callable = EACallable()
        ea_data["ea"].callbacks = [callable]
        _, res = ea_data["ea"].solve(ea_data["dataset"].data)
        ea_data["dataset"].res_lock.acquire()
        if ea_data["dataset"].threshold_cost > res:
            callable.save(ea_to_string(ea_data["ea"]), ea_data["dataset"].res_path)
        if ea_data["dataset"].best_cost > res:
            ea_data["dataset"].best_cost = res
            print(f"New best cost={res} ({ea_data['dataset'].gf_cost / res * 100:.2f}% of greedy result) time={callable.elapsed_time:.4f}s (gf_time={ea_data['dataset'].gf_time:.4f}s t_increase={callable.elapsed_time/ea_data['dataset'].gf_time * 100 - 100.:.2f}%) for {ea_to_string(ea_data['ea'])}")
        ea_data["dataset"].res_lock.release()

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
    parser.add_argument("-k", "--keys", dest="dataset_keys", type=str, required=True)
    parser.add_argument("-t", "--thread-percentage", dest="thread_percentage", type=float, default=0.9)
    parser.add_argument("-tc", "--threshold-cost", dest="threshold_cost", type=float, default=0.8)
    parser.add_argument("-ts", "--threshold-seconds", dest="threshold_seconds", type=float, default=1.5)
    parser.add_argument("-min_it", "--minimum", dest="min_it", type=int, default=25)
    parser.add_argument("-dir", "--directory", dest="dir", type=str, default="data/TSPLIB/export")
    parser.add_argument("-if", "--info-file", dest="info_file", type=str, default="_file_lengths.csv")
    args = parser.parse_args()
    print(args)
    if not args.info_file.endswith(".csv"):
        args.info_file += ".csv"

    datasets_info = load_datasets_info(args.dir, args.info_file)

    if not isinstance(args.dataset_keys, list):
        args.dataset_keys = args.dataset_keys.split(",")

    for k in args.dataset_keys:
        if k.endswith(".csv"):
            k = k.replace(".csv", "")
        if k.endswith(".tsp"):
            k = k.replace(".tsp", "")
        assert k in datasets_info.keys(), f"Dataset {k} not found in {args.info_file}"

    cpu_c = os.cpu_count() - 1 # -1 => main thread is also used
    cpu_c = int(max(1, min(args.thread_percentage * cpu_c, cpu_c)))
    print(f"Running {cpu_c} threads")

    os.makedirs(results_dir, exist_ok=True)
    is_active = True
    threads = []
    for i in range(cpu_c):
        thread = Thread(target=worker_function)
        threads.append(thread)
        thread.start()

    max_threads_data_size = cpu_c * 2
    for k in args.dataset_keys:
        current_info = datasets_info[k]
        dataset_data = DatasetData(name=k, res_path=os.path.join(results_dir, f"{k} {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.csv"), data=load_csv(os.path.join(args.dir, k + ".csv")), gf_cost=current_info['gf-cost'], gf_time=current_info['gf-time'], threshold_percentage=args.threshold_cost)
        threshold_seconds = current_info["gf-time"] * args.threshold_seconds
        print(f"Running {k} dataset, greedy first with {current_info['length']} cities to beat: cost={current_info['gf-cost']:.2f} time={current_info['gf-time']:.4f}s, threshold: cost={dataset_data.threshold_cost:.2f} time={threshold_seconds:.4f}s")
        assert len(dataset_data.data) == current_info["length"]
        if current_info["length"] < 3:
            continue
        previous_population_size = -1
        
        for cost_calculator in [ManhattanCostCalculation]: # FIXME: update to whatever is needed
            for crossover_type in [OrderCrossover, PartiallyMappedCrossover]: # FIXME: update to whatever is needed
                for population_size in range(3, 50, 1): # FIXME: update to whatever is needed
                # for __population_size in range(3, 101, 1): # FIXME: update to whatever is needed
                #     population_size = int(max(3, current_info["length"] * __population_size / 100.))
                #     if population_size == previous_population_size:
                #         continue
                    print(f"Starting population size={population_size} ({population_size/current_info['length']*100:.2f}%)")
                    # previous_population_size = population_size
                    previous_elite_size = -1
                    for __elite_size in range(1, 101, 1): # FIXME: update to whatever is needed
                        elite_size = max(2, min(int(population_size * __elite_size / 100.), population_size-1))
                        if elite_size == previous_elite_size:
                            continue
                        previous_elite_size = elite_size
                        previous_segment_length = -1
                        ea_data_lock.acquire()
                        ea_list.append({
                                "ea": EvolutionarySolver(
                                    elite_selector=EliteSelector(cost_calculator, elite_size=elite_size),
                                    crossover=crossover_type(None),
                                    stop_criterions=[TimeStopCriterion(threshold_seconds)],
                                    population_size=population_size,
                                    minimum_iterations=args.min_it
                                ),
                                "dataset": dataset_data
                            })
                        ea_data_lock.release()
                        for __segment_length in range(1, 101, 1): # FIXME: update to whatever is needed
                            segment_length = max(1, min(int(current_info["length"] * __segment_length / 100.), current_info["length"]-1))
                            if segment_length == previous_segment_length:
                                continue
                            previous_segment_length = segment_length
                            while True:
                                ea_data_lock.acquire()
                                if len(ea_list) < max_threads_data_size:
                                    break
                                ea_data_lock.release()
                                time.sleep(0.010)
                                continue
                            ea_list.append({
                                "ea": EvolutionarySolver(
                                    elite_selector=EliteSelector(cost_calculator, elite_size=elite_size),
                                    crossover=crossover_type(segment_length),
                                    stop_criterions=[TimeStopCriterion(threshold_seconds)],
                                    population_size=population_size,
                                    minimum_iterations=args.min_it
                                ),
                                "dataset": dataset_data
                            })
                            ea_data_lock.release()

    is_active = False
    print(f"Waiting for threads to finish")
    for thread in threads:
        thread.join()