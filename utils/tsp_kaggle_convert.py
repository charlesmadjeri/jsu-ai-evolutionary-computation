#!/bin/env/python

"""
This script is used to convert the TSP Kaggle dataset from https://www.kaggle.com/datasets/ziya07/traveling-salesman-problem-tsplib-dataset 
to a format that can be used by our application.
"""

import argparse
import ast
import csv
import os

def load_tsp_kaggle_data(file_path: str, instance_id: int) -> list[tuple[int, int]]:
    if not file_path.endswith('.csv'):
        raise ValueError('File must be a .csv file')
    if not os.path.exists(file_path):
        raise ValueError(f'File {file_path} does not exist')
    if instance_id < 0:
        raise ValueError(f'instance_id must be greater than 0')
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[0] == instance_id:
                result = ast.literal_eval(str(line[2]))
                result = [(int(i[0]), int(i[1])) for i in result]
                return result
        else:
            raise ValueError(f"{instance_id} was not found in '{file_path}'")




if __name__ == '__main__':
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    def generate_output_file_path():
        # go one up
        base_filename = 'data'
        result_filename = base_filename + '.csv'
        if not os.path.exists(os.path.join(parent_dir, result_filename)):
            return result_filename
        for i in range(1, 100):
            result_filename = base_filename + '_' + str(i) + '.csv'
            if not os.path.exists(os.path.join(parent_dir, result_filename)):
                return result_filename
        raise ValueError(f'Too many output files in {parent_dir}')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, default=os.path.join(parent_dir, 'dataset.csv'),
                        metavar='INPUT_CSV_PATH', 
                        help='CSV dataset path. The dataset is from https://www.kaggle.com/datasets/ziya07/traveling-salesman-problem-tsplib-dataset')
    parser.add_argument('-o', '--output', type=str, required=True, default=generate_output_file_path(), 
                        metavar='OUTPUT_CSV_PATH', 
                        help='Output file path')
    parser.add_argument('-w', '--where', type=str | int,
                        metavar='LOOKUP_SIZE',
                        help='Lookup size for the dataset size. Can be a number or range in format "10-20"')
    args = parser.parse_args()
    print(args)
    try:
        load_tsp_kaggle_data(args.file)
    except Exception as e:
        print(e)
        exit(1)
    exit(0)