#!/usr/bin/env python3

"""
This script is used to convert the TSP Kaggle dataset from https://www.kaggle.com/datasets/ziya07/traveling-salesman-problem-tsplib-dataset 
to a format that can be used by our application.

Example usage:
python tsp_kaggle_convert.py -i data/input_dataset.csv -o data/output_dataset.csv --id 1234
"""

import argparse
import csv
import os
import sys
import ast

"""
Loads the TSP Kaggle dataset from the given file path and returns the data for the given instance id.
"""
def load_tsp_kaggle_data(file_path: str, instance_id: int) -> list[tuple[float, float]]:
    if not file_path.endswith('.csv'):
        raise ValueError('File must be a .csv file')
    if not os.path.exists(file_path):
        raise ValueError(f'File {file_path} does not exist')
    if instance_id < 0:
        raise ValueError(f'instance_id must be greater than 0')
    # needed so it can process large datasets
    ORIGINAL_FIELD_SIZE_LIMIT = csv.field_size_limit()
    csv.field_size_limit(sys.maxsize)
    instance_id = str(instance_id)
    
    with open(file_path, 'r') as file:
        for _, line in enumerate(file, start=1):
            csv_line = next(csv.reader([line]))
            if csv_line[0] == instance_id:
                csv.field_size_limit(ORIGINAL_FIELD_SIZE_LIMIT)
                result = ast.literal_eval(str(csv_line[2]))
                return [(float(i[0]), float(i[1])) for i in result]
        else:
            csv.field_size_limit(ORIGINAL_FIELD_SIZE_LIMIT)
            raise ValueError(f'{instance_id} was not found in "{file_path}"')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, dest='input_path',
                        metavar='INPUT_CSV_PATH', 
                        help='input dataset path. The dataset is from https://www.kaggle.com/datasets/ziya07/traveling-salesman-problem-tsplib-dataset')
    parser.add_argument('-o', '--output', type=str, required=True, dest='output_path',
                        metavar='OUTPUT_CSV_PATH', 
                        help='output dataset export path')
    parser.add_argument('--id', type=int, required=True, dest='instance_id',
                        metavar='INSTANCE_ID',
                        help='instance_id from the input dataset specifying row for export')
    args = parser.parse_args()

    loaded_data = load_tsp_kaggle_data(args.input_path, args.instance_id)
    with open(args.output_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])
        for x, y in loaded_data:
            writer.writerow([x, y])



    #TODO: Deleteme! Just for testing
    # Construct the absolute path to the 'import' directory
    import_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Add the import directory to sys.path
    sys.path.append(import_dir)

    # Now you can import the module
    import load_csv
    loaded_data2 = load_csv.load_csv(args.output_path)
    assert loaded_data == loaded_data2