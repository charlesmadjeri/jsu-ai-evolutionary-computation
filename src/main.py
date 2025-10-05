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
    if parsed_data["verbose"] > 0:
        print(f"Solution: {solution_points}")
        print(f"Distance: {distance}")
    # TODO: Replace this with export_results 
    if parsed_data["export_image"]:
        generate_png_export.generate_png_export(solution_points)
    if parsed_data["export_csv"]:
        export_results.export_results(solution_points)
    return 0

if __name__ == "__main__":
    sys.exit(main())