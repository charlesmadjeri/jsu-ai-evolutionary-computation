#!/usr/bin/env python3
"""
Jonkoping School of Engineering (JTH)

Team Members:
- Aikeya Ainiwaer
- Andrej Kutny
- Charles Madjeri
- Samrat Debnath
- Vladimir Giustacchini

AI course - Evolutionary computation assignment
"""
import sys
import os

from export import export_results
from dataparser.arg_parser import main_parser, parse_main
from export.export_results import export_results

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main() -> int:
    try:
        parsed_data = parse_main()
    except Exception as e:
        print(f"Error: {e}")
        main_parser.print_help()
        return 1
    solution_indices, distance = parsed_data["solver"].solve(parsed_data["dataset"])
    solution_points = [parsed_data["dataset"][i] for i in solution_indices]
    verbose_level = parsed_data["verbose"]
    if verbose_level > 0:
        if verbose_level > 1:
            print(f"Solution points: {solution_points}")            
        print(f"Solution indices: {solution_indices}")
        print(f"Distance: {distance}")
    export_results(solution_points, distance, export_image=parsed_data["export_image"], export_csv=parsed_data["export_csv"])
    return 0

if __name__ == "__main__":
    sys.exit(main())