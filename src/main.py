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
import os
from typing import Optional


def display_help() -> None:
    print("Usage: python main.py <dataset_csv_file>")
    print("Example: python main.py dataset.csv")
    print("\nPlease provide a CSV dataset file as an argument.")


def validate_dataset_file(file_path: str) -> bool:
    if not file_path.lower().endswith('.csv'):
        print("Error: Please provide a CSV file (with .csv extension)")
        return False

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return False

    return True


def parse_arguments() -> Optional[str]:
    if len(sys.argv) != 2:
        display_help()
        return None

    file_path = sys.argv[1]
    return file_path if validate_dataset_file(file_path) else None


def process_dataset_file(dataset_file: str) -> None:
    print(f"Processing dataset file: {dataset_file}")
    # Add dataset processing logic here


def main() -> int:
    dataset_file = parse_arguments()
    if dataset_file is None:
        return 1

    process_dataset_file(dataset_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())