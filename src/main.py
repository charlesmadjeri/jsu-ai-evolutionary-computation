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

import sys
from typing import Optional
import load_csv

def display_help() -> None:
    print("Usage: python main.py <dataset_csv_file>")
    print("Example: python main.py dataset.csv")
    print("\nPlease provide a CSV dataset file as an argument.")


def parse_arguments() -> Optional[str]:
    if len(sys.argv) != 2:
        display_help()
        return None

    return sys.argv[1]

def main() -> int:
    input_path = parse_arguments()
    if input_path is None:
        return 1

    input_data = load_csv.load_csv(input_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())