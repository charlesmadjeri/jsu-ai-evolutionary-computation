# Traveling Salesman Problem Solver

## Overview
This project provides a comprehensive implementation of the Traveling Salesman Problem (TSP) using evolutionary computation algorithms, with additional support for greedy-first algorithms and advanced parameter fine-tuning capabilities.

## Project Structure

- `data/` – Dataset files (`.csv` format and TSPLIB `.tsp` format)
- `src/` – All source code
  - `main.py` – Main TSP solver entry point
  - `fine_tuning.py` – Parameter optimization script
  - `fine_tuning/` – Fine-tuning system modules
  - `solvers/` – Algorithm implementations (evolutionary, greedy-first)
  - `cost_calculation/` – Distance calculation methods (Manhattan, Euclidean)
  - `crossover/` – Crossover operators (Order, Partially Mapped)
  - `stop_criterions/` – Stopping criteria implementations
  - `export/` – Result export functionality
- `results/` – Output directory for solver results and fine-tuning data
  - `simple_passes/` – Individual algorithm runs
  - `fine-tuning/` – Parameter optimization results
  - `baseline/` – Baseline comparison data
- `tests/` – Unit and integration tests
- `docs/` – Project documentation

## Features

- **Evolutionary Algorithm**: Advanced genetic algorithm with configurable parameters
- **Greedy-First Algorithm**: Basic heuristic for comparison purposes
- **Parameter Fine-Tuning**: Automated parameter optimization system
- **Multiple Distance Metrics**: Manhattan and Euclidean distance calculations
- **Flexible Crossover**: Order and Partially Mapped crossover operators
- **Comprehensive Logging**: Multiple verbosity levels with structured output
- **Statistical Analysis**: Automatic baseline comparison and performance metrics
- **Parallel Processing**: Multi-core support for parameter optimization

***
## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/charlesmadjeri/jsu-ai-evolutionary-computation.git
   cd jsu-ai-evolutionary-computation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the TSP Solver

#### Basic Usage
```bash
# Run with default parameters
python src/main.py data/a280.csv

# Run with custom parameters
python src/main.py data/a280.csv -ps 100 -es 0.15 -sit 200 -sim 0.001
```

#### Algorithm Examples
```bash
# Evolutionary algorithm with Manhattan distance
python src/main.py data/a280.csv -ps 50 -es 0.2 -cr order -cc manhattan --verbose 2

# Evolutionary algorithm with Euclidean distance
python src/main.py data/a280.csv -ps 80 -es 0.1 -cr partially-ordered -cc euclidean --verbose 1

# Greedy-first algorithm for comparison
python src/main.py data/a280.csv -gf --verbose 1

# Export results as CSV and PNG
python src/main.py data/a280.csv -e csv png -ps 60 -es 0.25
```

#### Verbosity Levels
- `--verbose 1`: Essential results only (recommended for scripts)
- `--verbose 2`: Include improvement notifications
- `--verbose 3`: Detailed iteration-by-iteration progress

### Fine-Tuning Parameters

The project includes an advanced parameter optimization system that automatically finds the best algorithm parameters for your datasets.

#### Running Parameter Fine-Tuning
```bash
# Basic fine-tuning (tests 20 parameter sets with 25 trials each)
python src/fine_tuning.py data/a280.csv

# Custom number of parameter sets
python src/fine_tuning.py data/a280.csv -n 10

# Fine-tune multiple datasets
python src/fine_tuning.py data/berlin52.csv -n 15
python src/fine_tuning.py data/kroA100.csv -n 25
```

#### Fine-Tuning Output
The fine-tuning system creates timestamped folders in `results/fine-tuning/` containing:
- `fine_tuning_{dataset}.json` - Complete results with all trial data
- `summary_{dataset}.csv` - Statistical summary for analysis
- `convergence_{dataset}.csv` - Iteration-by-iteration convergence data

#### Configuring Fine-Tuning Parameters
Edit `src/fine_tuning/config.py` to modify:

```python
class Config:
    MIN_TRIALS = 25  # Number of trials per parameter set
    ALGORITHM_TIMEOUT = 300  # Timeout per trial (seconds)
    
    # Parameter search ranges
    PARAM_RANGES = {
        'population_size': (20, 200),
        'elite_size': (0.05, 0.4),
        'crossover_segment': (0.1, 0.7),
        'stop_iterations': (50, 300),
        'stop_improvement': (0.0001, 0.01)
    }
    
    # Exploration vs exploitation balance
    EXPLOITATION_PROBABILITY = 0.7  # 70% near best, 30% random exploration
    EXPLORATION_VARIANCE = 0.15     # Gaussian variance for exploration
```

### Command Reference

#### Main Algorithm Parameters
Run `python src/main.py -h` for complete help:

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

## Dataset Format

The solver accepts CSV files with city coordinates:

```csv
x,y
256.0,141.0
124.0,69.0
180.0,117.0
```

Each row represents a city with x,y coordinates. The solver automatically calculates distances between all city pairs.

### Sample Datasets
- `data/a280.csv` - 280-city problem
- `data/TSPLIB/` - Standard TSPLIB benchmark instances

## Output Files

### Algorithm Results (`results/simple_passes/TIMESTAMP/`)
- `results.csv` - Complete solution with coordinates and total distance
- `results.png` - Visualization of the optimal route

### Fine-Tuning Results (`results/fine-tuning/TIMESTAMP/`)
- `fine_tuning_{dataset}.json` - Detailed results with convergence data
- `summary_{dataset}.csv` - Statistical analysis ready for reports
- `convergence_{dataset}.csv` - Iteration-by-iteration performance data

## Performance Metrics

The system automatically calculates and exports:
- **Best Solution Quality**: Shortest path found across all runs
- **Average Solution Quality**: Mean path length for consistency analysis  
- **Standard Deviation**: Algorithm robustness indicator
- **Computational Time**: Average execution time per run
- **Convergence Behavior**: Solution quality evolution over iterations
- **Baseline Comparison**: Performance gap vs. known optimal solutions

## Advanced Configuration

### Algorithm Parameters
- `population_size` (-ps): Population size (integer or percentage of cities)
- `elite_size` (-es): Elite population percentage (0.0-1.0)
- `crossover_type` (-cr): `order` or `partially-ordered`
- `crossover_segment` (-cs): Crossover segment length
- `stop_iterations` (-sit): Maximum iterations
- `stop_improvement` (-sim): Minimum improvement threshold
- `cost_calculator` (-cc): `manhattan` or `euclidean` distance

### Stopping Criteria
The algorithm stops when ANY of these conditions are met:
- Maximum iterations reached (`-sit`)
- Improvement below threshold (`-sim`)
- Time limit exceeded (`-shr`, `-smin`, `-ssec`)
- Cost threshold reached (`-st`)

***




## Examples for experiment

### Comparing Distance Metrics
```bash
# Manhattan distance
python src/main.py data/a280.csv -cc manhattan -ps 100 -es 0.2 --verbose 1

# Euclidean distance  
python src/main.py data/a280.csv -cc euclidean -ps 100 -es 0.2 --verbose 1
```

### Crossover Operator Comparison
```bash
# Order crossover
python src/main.py data/a280.csv -cr order -cs 0.3 --verbose 2

# Partially mapped crossover
python src/main.py data/a280.csv -cr partially-ordered -cs 0.3 --verbose 2
```

### Statistical Analysis Workflow
```bash
# 1. Run fine-tuning to find optimal parameters
python src/fine_tuning.py data/a280.csv -n 20

# 2. Use discovered parameters for multiple runs
python src/main.py data/a280.csv -ps 85 -es 0.15 -cs 0.25 --verbose 1

# 3. Results are automatically compared to baselines in results/baseline/
```

## Contributors
- **Aikeya Ainiwaer**
- **Andrej Kutny** 
- **Charles Madjeri**
- **Samrat Debnath**
- **Vladimir Giustacchini**

***

*Jönköping School of Engineering (JTH) - AI Course - Evolutionary Computation Assignment*
