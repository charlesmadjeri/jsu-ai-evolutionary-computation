from argparse import ArgumentParser
import os
from random import randint

parser = ArgumentParser(
    description="Generate a dataset of random nodes and save it to a TSP file."
)
parser.add_argument(
    "-n", "--number-of-nodes",
    dest="number_of_nodes",
    type=lambda x: int(x) if int(x) > 1000 and int(x) <= 1000000 else 10000,
    default=100000,
    help="Number of nodes to generate (1000-1000000). Default is 100000.",
)
parser.add_argument(
    "-min", "--min-value",
    dest="min_value",
    type=lambda x: int(x) if int(x) >= 0 and int(x) <= 100000 else 20000,
    default=20000,
    help="Minimum value for coordinates (0-100000). Default is 20000.",
)
parser.add_argument(
    "-max", "--max-value",
    dest="max_value",
    type=lambda x: int(x) if int(x) > 100000 and int(x) <= 1000000 else 500000,
    default=500000,
    help="Maximum value for coordinates (100000-1000000). Default is 500000.",
)
parser.add_argument(
    "--name",
    dest="name",
    type=str,
    help="Output file name. Its value will be saved in the results/generated_datasets folder.",
    required=True
)

args = parser.parse_args()
nr_nodes = args.number_of_nodes
min_value = args.min_value
max_value = args.max_value
file_name = args.name  
dataset = []

if not os.path.exists("results/generated_datasets"):
    os.makedirs("results/generated_datasets")

if os.path.exists(f"results/generated_datasets/{file_name}.tsp"):
    raise FileExistsError(f"Error: File 'results/generated_datasets/{file_name}.tsp' already exists.")

with open(f"results/generated_datasets/{file_name}.tsp", "w") as file:
    file.write("x,y\n")
    for i in range(nr_nodes):
        rand_tuple = tuple((randint(min_value, max_value), randint(min_value, max_value)))
        while rand_tuple in dataset:
            rand_tuple = tuple((randint(min_value, max_value), randint(min_value, max_value)))
        else:
            dataset.append(rand_tuple)
            file.write(f"{rand_tuple[0]},{rand_tuple[1]}\n")