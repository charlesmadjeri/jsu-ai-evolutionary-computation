import argparse
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
    return (min is None or min < value) and (max is None or value < max)

"""
Check if the value is an integer and is in the range [min, max]
Returns the value if it is a valid integer, otherwise returns None
Raises an argparse.ArgumentTypeError if the value is not in range
"""
def int_checker(value, min, max):
    if isinstance(value, int):
        if not range_checker(value, min, max):
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer in range {range_to_str(min, max)}")
        return value
    return None

"""
Check if the value is a float and is in the range [min, max]
Returns the value if it is a valid float, otherwise returns None
Raises an argparse.ArgumentTypeError if the value is not in range
"""
def float_checker(value, min, max):
    if isinstance(value, float):
        if not range_checker(value, min, max):
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid float in range {range_to_str(min, max)}")
        return value
    return None

"""
Checks if the value is an integer or a float using int_checker and float_checker
"""
def int_or_float_checker(value, int_min, int_max, float_min, float_max):
    int_res = int_checker(value, int_min, int_max)
    return int_res if int_res is not None else float_checker(value, float_min, float_max)

def stopping_criterion_checker(value, min, max):
    def print_help_and_raise():
        # TODO: Print help
        print("TODO")
        raise argparse.ArgumentTypeError("Failed to parse stopping criterion")

    if not isinstance(value, list):
        print_help_and_raise()
    
    end = value[-1]
    if isinstance(end, str):
        end = end.lower()
        if end in ['iter', 'iterations']:
            if len(value) != 2 or not isinstance(value[0], int):
                print_help_and_raise()
            #TODO: Return object for stopping criterion for iterations
            raise NotImplementedError("Not implemented")
        if end in ['seconds', 'sec']:
            if len(value) != 2 or not isinstance(value[0], int):
                print_help_and_raise()
            #TODO: Return object for stopping criterion for seconds
            raise NotImplementedError("Not implemented")
        if end in ['minutes', 'min']:
            if len(value) != 2 or not isinstance(value[0], int):
                print_help_and_raise()
            #TODO: Return object for stopping criterion for minutes
            raise NotImplementedError("Not implemented")
        if end in ['hours', 'hour', 'hrs', 'hr']:
            if len(value) != 2 or not isinstance(value[0], int):
                print_help_and_raise()
            #TODO: Return object for stopping criterion for hours
            raise NotImplementedError("Not implemented")
        if end in ['improvement']:
            if len(value) != 2 or not isinstance(value[0], float):
                print_help_and_raise()
            #TODO: Return object for stopping criterion for improvement
            raise NotImplementedError("Not implemented")
    print_help_and_raise()
            


"""
Main parser for the application
"""
def main_parser(args=None):
    parser = argparse.ArgumentParser(
        description='Solver for the Traveling Salesman Problem (TSP) using Evolutionary Computation'
    )
    parser.add_argument('-e', '--export', choices=['png', 'csv'], default=['png', 'csv'], nargs='+')
    parser.add_argument('input_path', type=str,
                        metavar='INPUT_CSV_PATH', 
                        help='Dataset path, should be .csv file containing 2 columns for x and y coordinates, rows representing cities')
    #TODO: implement 
    parser.add_argument('-ps', '--population-size', dest='population_size',
                        type=lambda x: int_or_float_checker(x, int_min=1, int_max=None, float_min=0, float_max=1), 
                        help=f'Size of the solution population size - if percentage, must be in range {range_to_str(0, 1)}, if integer, must be in range {range_to_str(1, None)}', default=10)
    parser.add_argument('-es', '--elite-size', dest='elite_size',
                        type=lambda x: float_checker(x, min=0, max=1), 
                        help=f'Size of the elite population - it is percentage and must be in range {range_to_str(0, 1)}', default=.1)
    parser.add_argument('-cs', '--crossover-segment-lenght', dest='crossover_size',
                        type=lambda x: int_or_float_checker(x, int_min=1, int_max=None, float_min=0, float_max=1), 
                        help=f'Segment length for crossover - if percentage, must be in range {range_to_str(0, 1)}, if integer, must be in range {range_to_str(1, None)}', default=5)
    parser.add_argument('-mp', '--mutation-probability', dest='mutation_probability',
                        type=lambda x: float_checker(x, min=0, max=1), 
                        help=f'Probability of mutation - must be in range {range_to_str(0, 1)}', default=.05)
    parser.add_argument('-ms', '--mutation-step-size', dest='mutation_step_size',
                        type=lambda x: int_checker(x, min=0, max=None), 
                        help=f'Step size for mutation - must be in range {range_to_str(0, None)}', default=2)
    
    parser.add_argument('-v', action='count', default=0, dest='verbose', help='Verbose level (described by count of \'v\' characters)')
    parser.add_argument('--verbose', type=int, dest='verbose', help='Verbose level (described by value)')
    parsed_args = parser.parse_args(args)
    print(parsed_args)
    return parsed_args