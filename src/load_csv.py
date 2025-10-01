"""
Loading CSV file in EXPECTED format. Can handle both with and without header.

Example csv:
x,y
51.984470473161224,96.71323760176688
58.5967496647723,61.18848278655511
45.04572417479401,97.653961616284
44.603211190532846,90.44637365709606
48.90738291765828,3.5264341745102734
74.88306077395245,47.81196924100425
53.967466142465035,35.39663160833789
"""

import csv

def load_csv(file_path: str) -> list[tuple[float, float]]:
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        first_row = next(reader, None)
        if len(first_row) != 2:
            raise ValueError(f'First row must contain 2 columns, got {len(first_row)}, are you using processed .csv file?')
        if first_row != ['x', 'y']:
            result = [(float(first_row[0]), float(first_row[1]))]
        else:
            result = []
        return result + [(float(row[0]), float(row[1])) for row in reader]
