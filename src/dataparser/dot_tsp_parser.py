import argparse
import os
import re

def load_tsp_data(file_path: str) -> list[tuple[float, float]]:
    if not file_path.endswith(".tsp"):
        raise ValueError("File must be a .tsp file")
    if not os.path.exists(file_path):
        raise ValueError(f"File {file_path} does not exist")
    
    node_coord_section = False
    nodes = []

    with open(file_path, "r") as file:
        while True:
            try: 
                line = file.readline()
                if "EOF" in line or re.sub(" +", " ", line) == "\n": # in case no EOF is declared, ex: usa13509
                    break
                if node_coord_section == True:
                    split_line = [re.sub(" +", " ", line).strip().split(" ")[1], re.sub(" +", " ", line).strip().split(" ")[2]]
                    for idx_split in range(2):
                        if isinstance(split_line[idx_split], str):
                            try:
                                split_line[idx_split] = float(split_line[idx_split])
                            except ValueError:
                                split_line[idx_split] = int(split_line[idx_split])
                    nodes.append(tuple(split_line))
                else:
                    node_coord_section = "NODE_COORD_SECTION" in line
            except IndexError:
                break
    if nodes == []:
        raise TypeError("Error: Could not retrieve a list of (x, y) coordinates. Try using a file with NODE_COORD_SECTION")
    return nodes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, dest="input_path",
                        metavar="INPUT_TSP_PATH", 
                        help="input dataset path")
    parser.add_argument("-o", "--output", type=str, required=True, dest="output_path",
                        metavar="OUTPUT_TSP_PATH", 
                        help="output dataset export path")
    args = parser.parse_args()

    loaded_data = load_tsp_data(args.input_path)

    with open(args.output_path, "w") as file:
        file.write("x,y\n")
        for x, y in loaded_data:
            file.write(f"{x},{y}\n")