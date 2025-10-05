from argparse import ArgumentTypeError, ArgumentParser

from crossover.order_crossover import OrderCrossover
from crossover.partially_mapped_crossover import PartiallyMappedCrossover
from elite_selector.elite_selector import EliteSelector
from load_csv import load_csv
from solvers.evolutionary_solver import EvolutionarySolver
from stop_criterions.time_stop_criterion import TimeStopCriterion
from stop_criterions.improvement_stop_criterion import ImprovementStopCriterion
from stop_criterions.iterations_stop_criterion import IterationsStopCriterion

from cost_calculation.manhattan_cost_calculation import ManhattanCostCalculation
from cost_calculation.euclidean_cost_calculation import EuclideanCostCalculation

from solvers.greedy_first import GreedyFirst

from os import path

"""
Stringify the range [min, max]
"""
def range_to_str(min, max):
    return f"[{"-inf" if min is None else min}, {"inf" if max is None else max}]"

"""
Check if the value is in the range [min, max]
Returns True if the value is in range, otherwise returns False
"""
def range_checker(value, min, max):
    if value is None:
        return min is None and max is None
    return (min is None or min <= value) and (max is None or value <= max)

"""
Returns True if the value is strict float (not integer), otherwise returns False
"""
def check_is_float(value):
    if isinstance(value, int):
        return False
    if isinstance(value, float):
        return True
    if isinstance(value, str):
        try:
            if value.isalnum():
                raise ValueError(f"'{value}' is int")
            value = float(value)
        except ValueError:
            return False
        return True

"""
Check if the value is an integer and is in the range [min, max]
Returns the value if it is a valid integer, otherwise returns None
Raises an argparse.ArgumentTypeError if the value is not in range
"""
def int_checker(value, min, max):
    if value is None:
        return None
    
    if check_is_float(value):
        return None
    
    try:
        value = int(value)
    except ValueError:
        return None
    
    if not range_checker(value, min, max):
        raise ArgumentTypeError(f"'{value}' is not a valid integer in range {range_to_str(min, max)}")
    return value

"""
Check if the value is a float and is in the range [min, max]
Returns the value if it is a valid float, otherwise returns None
Raises an argparse.ArgumentTypeError if the value is not in range
"""
def float_checker(value, min, max):
    if value is None:
        return None
    
    if not check_is_float(value):
        return None
    
    try:
        value = float(value)
    except ValueError:
        return None

    if not range_checker(value, min, max):
        raise ArgumentTypeError(f"'{value}' is not a valid float in range {range_to_str(min, max)}")
    return value

"""
Checks if the value is an integer or a float using int_checker and float_checker
"""
def int_or_float_checker(value, int_min, int_max, float_min, float_max, none_allowed=False):
    if isinstance(value, str) and value.lower() == "none":
        value = None

    if value is None:
        if none_allowed:
            return None
        raise ArgumentTypeError("None value is not allowed")
    
    int_res = int_checker(value, int_min, int_max)
    result = int_res if int_res is not None else float_checker(value, float_min, float_max)
    if result is None:
        raise ArgumentTypeError(f"'{value}' is not a valid integer or float in range int{range_to_str(int_min, int_max)} float{range_to_str(float_min, float_max)}")
    return result

main_parser = ArgumentParser(
    description='Solver for the Traveling Salesman Problem (TSP) using Evolutionary Computation'
)
main_parser.add_argument('-e', '--export', choices=['png', 'csv'], default=['png', 'csv'], nargs='+')
main_parser.add_argument('input_path', type=str,
                    metavar='INPUT_CSV_PATH', 
                    help='Dataset path, should be .csv file containing 2 columns for x and y coordinates, rows representing cities')
# --population-size 3 because has to have 2 parents and 1+ child
main_parser.add_argument('-ps', '--population-size', dest='population_size',
                    type=lambda x: int_or_float_checker(x, int_min=3, int_max=None, float_min=0, float_max=1),
                    help=f'Size of the solution population size - if percentage, must be in range {range_to_str(0, 1)}, if integer, must be in range {range_to_str(1, None)}', default=10)
main_parser.add_argument('-es', '--elite-size', dest='elite_size',
                    type=lambda x: int_or_float_checker(x, int_min=2, int_max=None, float_min=0, float_max=1), 
                    help=f'Size of the elite population - it is percentage and must be in range {range_to_str(0, 1)}', default=.1)
# TODO: --crossover-segment can be also None => randomly generated segment - implement if agreed
main_parser.add_argument('-cr', '--crossover-type', dest='crossover_type', choices=['order', 'partially-ordered'], default='order')
main_parser.add_argument('-cs', '--crossover-segment', dest='crossover_segment',
                    type=lambda x: int_or_float_checker(x, int_min=1, int_max=None, float_min=0, float_max=1, none_allowed=True), 
                    help=f'Segment length for crossover - if percentage, must be in range {range_to_str(0, 1)}, if integer, must be in range {range_to_str(1, None)}', default=5)
# main_parser.add_argument('-mp', '--mutation-probability', dest='mutation_probability',
#                     type=lambda x: float_checker(x, min=0, max=1), 
#                     help=f'Probability of mutation - must be in range {range_to_str(0, 1)}', default=.001)
# main_parser.add_argument('-ms', '--mutation-step-size', dest='mutation_step_size',
#                     type=lambda x: int_checker(x, min=0, max=None), 
#                     help=f'Step size for mutation - must be in range {range_to_str(0, None)}', default=2)
main_parser.add_argument('-sit', '--stop-iterations', required=False, dest='stop_iterations',
                    type=lambda x: int_checker(x, min=1, max=None), 
                    help='Stoppage criterion for number of iterations.')
main_parser.add_argument('-shr', '--stop-hours', required=False, dest='stop_hours', type=int,
                    help='Stoppage criterion for hours. If minutes and/or seconds are also provided, it will be added to the total time.')
main_parser.add_argument('-smin', '--stop-minutes', required=False, dest='stop_minutes', type=int, 
                    help='Stoppage criterion for minutes. If seconds and/or hours are also provided, it will be added to the total time.')
main_parser.add_argument('-ssec', '--stop-seconds', required=False, dest='stop_seconds', type=int,
                    help='Stoppage criterion for seconds. If minutes and/or hours are also provided, it will be added to the total time.')
main_parser.add_argument('-sim', '--stop-improvement', required=False, dest='stop_improvement',
                    type=lambda x: float_checker(x, min=0.000000001, max=None),
                    help=f'Stoppage criterion for improvement - must be in range {range_to_str(0.000000001, None)}')
main_parser.add_argument('-cc', '--cost-calculator', dest='cost_calculator', choices=['manhattan', 'euclidean'], default='manhattan')
# parser.add_argument('-op', '--optimise-cost', dest='optimise_cost', choices=['min', 'max'], default='min') # temporarily disabled - evolutionary computation doesn't support max price (yet)
main_parser.add_argument('-gf', '--greedy-first', action='store_true', help='Use greedy first algorithm instead of evolutionary computation. WARNING: This will override most of the other arguments and run greedy first instead of evolutionary computation.', default=False)
main_parser.add_argument('-v', action='count', default=0, dest='verbose', help='Verbose level (described by count of \'v\' characters)')
main_parser.add_argument('--verbose', type=int, dest='verbose', help='Verbose level (described by value)')

"""
Main parser for the application
"""
def parse_main(args=None):
    parsed_args = main_parser.parse_args(args)

    dataset = load_csv(parsed_args.input_path)
    if len(dataset) == 0:
        raise ValueError(f"File {parsed_args.input_path} is empty")
    
    if not path.exists(parsed_args.input_path):
        raise ValueError(f"File {parsed_args.input_path} does not exist")
    if not parsed_args.input_path.endswith('.csv'):
        raise ValueError(f"File {parsed_args.input_path} is not a .csv file")
    

    if parsed_args.cost_calculator == 'manhattan':
        cost_calculator = ManhattanCostCalculation
    elif parsed_args.cost_calculator == 'euclidean':
        cost_calculator = EuclideanCostCalculation
    else:
        raise ValueError(f"Invalid distance calculator: {parsed_args.cost_calculator}")
    
    result = {
        "dataset": dataset,
        "verbose": parsed_args.verbose,
        "export_image": "png" in parsed_args.export,
        "export_csv": "csv" in parsed_args.export
    }

    minimise_cost = True
    # TODO: removed until evolutionary computation supports max price
    # minimise_cost = parsed_args.optimise_cost == 'min'

    if parsed_args.greedy_first:
        print("Using greedy first algorithm instead of evolutionary computation. WARNING: This will override most of the other arguments and run greedy first instead of evolutionary computation.")
        result["solver"] = GreedyFirst(cost_calculator=cost_calculator, minimise_cost=minimise_cost)
        return result

    population_size = parsed_args.population_size
    cities_count = len(dataset)
    if isinstance(population_size, float):
        population_size = max(3, int(.5 + population_size * cities_count))
    
    elite_size = parsed_args.elite_size
    if isinstance(elite_size, float):
        elite_size = max(2, min(int(.5 + elite_size * population_size), population_size - 1))

    segment_length = parsed_args.crossover_segment
    if isinstance(segment_length, float):
        segment_length = max(1, min(int(.5 + segment_length * cities_count), cities_count - 1))
    elif isinstance(segment_length, int):
        if segment_length >= cities_count:
            raise ValueError(f"Invalid crossover segment length: {segment_length}")

    if parsed_args.crossover_type == 'order':
        crossover = OrderCrossover(segment_length)
    elif parsed_args.crossover_type == 'partially-ordered':
        crossover = PartiallyMappedCrossover(segment_length)
    else:
        raise ValueError(f"Invalid crossover type: {parsed_args.crossover_type}")
    
    stoppage_criteria = []
    if parsed_args.stop_iterations is not None:
        stoppage_criteria.append(IterationsStopCriterion(parsed_args.stop_iterations))
    if parsed_args.stop_hours is not None or parsed_args.stop_minutes is not None or parsed_args.stop_seconds is not None:
        total_stop_seconds = 0
        total_stop_seconds += parsed_args.stop_hours * 3600 if parsed_args.stop_hours is not None else 0
        total_stop_seconds += parsed_args.stop_minutes * 60 if parsed_args.stop_minutes is not None else 0
        total_stop_seconds += parsed_args.stop_seconds if parsed_args.stop_seconds is not None else 0
        if total_stop_seconds > 0:
            stoppage_criteria.append(TimeStopCriterion(total_stop_seconds))
        else:
            print(f"Warning: total stop seconds is not greater than 0 ({total_stop_seconds}) - no time stop criterion will be used!")
    if parsed_args.stop_improvement is not None:
        stoppage_criteria.append(ImprovementStopCriterion(parsed_args.stop_improvement))
    if len(stoppage_criteria) == 0:
        raise ValueError("No stoppage criteria provided!")

    result["solver"] = EvolutionarySolver(
        elite_selector=EliteSelector(cost_calculator=cost_calculator, elite_size=elite_size), 
        crossover=crossover, 
        stop_criterions=stoppage_criteria, 
        population_size=population_size,
        verbose_level=result["verbose"]
    )
    return result