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
import argparse
import sys
from pathlib import Path

from fine_tuning.tuner import TSPFineTuner

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='TSP Fine-Tuning script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python fine_tuning.py data/a280.csv -n 10
    python fine_tuning.py data/berlin52.csv -n 20
        """
    )
    parser.add_argument(
        'input_file',
        help='Path to input CSV dataset'
    )
    parser.add_argument(
        '-n', '--num-parameter-sets',
        type=int,
        default=20, 
        help='Number of parameter sets to test (default: 20)'
    )
    
    return parser

def validate_arguments(args) -> None:
    if args.num_parameter_sets <= 0:
        print("[ERROR] Number of parameter sets must be greater than 0")
        sys.exit(1)
    
    if not Path(args.input_file).exists():
        print(f"[ERROR] Input file not found: {args.input_file}")
        sys.exit(1)
    
    if not args.input_file.endswith('.csv'):
        print(f"[ERROR] Input file must be a .csv file: {args.input_file}")
        sys.exit(1)

def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    
    validate_arguments(args)
    
    print("TSP evolutionary algorithm fine-tuning script")
    print("=" * 50)
    
    tuner = TSPFineTuner(args.input_file, args.num_parameter_sets)
    tuner.run()

if __name__ == "__main__":
    main()
