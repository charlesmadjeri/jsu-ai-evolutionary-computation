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
Samrat Debanath
Vladimir Giustacchini
Aikeya Ainiwaer
***