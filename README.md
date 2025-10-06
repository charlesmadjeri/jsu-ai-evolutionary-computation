#  Traveling Salesman Problem Solver
### Folder Descriptions:

- `.github/` – GitHub settings and CI workflows  
- `data/` – Dataset files (e.g., `dataset.csv`)  
- `docs/` – Project documentation  
- `src/` – All source code  
  - `main.py` – Entry point  
  - `solvers/` – Algorithm implementations (e.g., greedy, 2-opt)  
  - `import/` & `export/` – Handle I/O for data and results  
  - `utils/` – Utility functions  
- `tests/` – Unit and integration tests  
- `requirements.txt` – Python dependencies  
- `README.md`, `PROCESS.md`, `.gitignore`, etc.
*** 


 ### Description: 
 This project provides an implementation of the classic Traveling Salesman Problem (TSP), with a focus on a Genetic Algorithm (GA) as the primary solver, and one basic algorithm (e.g., greedy-first algorithm) for performance comparison purposes.
***
### Features:

* Greedy-first solver algorithm
* Evolutionary solver algorithm

***
Installation & Usage:


1. Clone the repository


`git clone https://github.com/charlesmadjeri/jsu-ai-evolutionary-computation.git
cd jsu-ai-evolutionary-computation`


2. Install dependencies


`pip install -r requirements.txt`


3. Run the script

To run the project, provide a dataset file (e.g. `data.csv`) as a command-line argument:

`python src/main.py data.csv`

Replace `data.csv` with the path to your dataset file.

Run `python src/main.py -h` to get help message:

```text
usage: main.py [-h] [-e {png,csv} [{png,csv} ...]] [-ps POPULATION_SIZE] [-es ELITE_SIZE] [-cr {order,partially-ordered}] [-cs CROSSOVER_SEGMENT] [-sit STOP_ITERATIONS] [-shr STOP_HOURS] [-smin STOP_MINUTES] [-ssec STOP_SECONDS] [-sim STOP_IMPROVEMENT] [-cc {manhattan,euclidean}] [-gf] [-v] [--verbose VERBOSE] INPUT_CSV_PATH

Solver for the Traveling Salesman Problem (TSP) using Evolutionary Computation

positional arguments:
  INPUT_CSV_PATH        Dataset path, should be .csv file containing 2 columns for x and y coordinates, rows representing cities

options:
  -h, --help            show this help message and exit
  -e, --export {png,csv} [{png,csv} ...]
  -ps, --population-size POPULATION_SIZE
                        Size of the solution population size - if percentage, must be in range [0, 1], if integer, must be in range [1, inf]
  -es, --elite-size ELITE_SIZE
                        Size of the elite population - it is percentage and must be in range [0, 1]
  -cr, --crossover-type {order,partially-ordered}
  -cs, --crossover-segment CROSSOVER_SEGMENT
                        Segment length for crossover - if percentage, must be in range [0, 1], if integer, must be in range [1, inf]
  -sit, --stop-iterations STOP_ITERATIONS
                        Stoppage criterion for number of iterations.
  -shr, --stop-hours STOP_HOURS
                        Stoppage criterion for hours. If minutes and/or seconds are also provided, it will be added to the total time.
  -smin, --stop-minutes STOP_MINUTES
                        Stoppage criterion for minutes. If seconds and/or hours are also provided, it will be added to the total time.
  -ssec, --stop-seconds STOP_SECONDS
                        Stoppage criterion for seconds. If minutes and/or hours are also provided, it will be added to the total time.
  -sim, --stop-improvement STOP_IMPROVEMENT
                        Stoppage criterion for improvement - must be in range [1e-09, inf]
  -cc, --cost-calculator {manhattan,euclidean}
  -gf, --greedy-first   Use greedy first algorithm instead of evolutionary computation. WARNING: This will override most of the other arguments and run greedy first instead of evolutionary computation.
  -v                    Verbose level (described by count of 'v' characters)
  --verbose VERBOSE     Verbose level (described by value)
```

***


###  Dataset format

The dataset must be a CSV file with the following columns:

-   `instance_id`
    
-   `num_cities`
    
-   `city_coordinates`
    
-   `distance_matrix`
    
-   `best_route`
    
-   `total_distance`
***


###  Output files

- CSV file of the computed route
- Visualization map of points and path solution (PNG picture)

These will be saved in the `outputs/` directory.




### Contributors:
Andrej Kutny
Charles Madjeri
Samrat Debnath
Vladimir Giustacchini
Aikeya Ainiwaer
***
