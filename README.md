# K-Coloring Algorithms Analysis

## Overview
This project analyzes various graph coloring algorithms, including Brute Force, Greedy, DSatur, and Welsh-Powell. The repository contains:
- Graph generation scripts for creating test cases.
- Implementations of graph coloring algorithms.
- Performance evaluation and visualization tools.
- Thesis documentation written in LaTeX.

## Repository Structure

K-Coloring-Algorithms-Analysis/
├── generated_tests/       # Automatically generated test cases
├── src/                   # Source code for algorithms
├── reports/               # Evaluation reports
├── thesis/                # LaTeX thesis files
├── README.md              # Project documentation
├── requirements.txt       # Dependencies
├── generate_graphs.py     # Graph generation script
├── run_tests.py           # Test execution script
└── visualize_results.py   # Performance visualization script


## Test Case Generation
The `generate_graphs.py` script generates the following graph types:

### Graph Types
- **Complete Graphs**
- **Bipartite Graphs**
- **Erdős–Rényi Random Graphs**
- **Chordal Graphs**
- **Planar Graphs (Grid Approximation)**
- **Slightly Hard-to-Color (SHC) Graphs**

### Installation
```bash
pip install -r requirements.txt
```

### 1. **`algorithms`**
Here are the implementation of alghortims :
- **Backtracking**
- **Greedy**
- **DSATUR**
- **Welsh-Powell**

Aceste implementaripot fi utilizate individual

Este important de precizat faptul ca am luat codurile de pe GeekForGeeks, de la urmatoarele link uri
- https://www.geeksforgeeks.org/graph-coloring-algorithm-in-python/
- https://www.geeksforgeeks.org/dsatur-algorithm-for-graph-coloring/
- https://www.geeksforgeeks.org/welsh-powell-graph-colouring-algorithm/
- https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/ 

Algoritmii au fost modificati, astfel incat sa nu functioneze pt grafuri hardcodate ci sa preia graf ul din fisierele de test.

### 2. **`generate_graphs.py`** 
Script for generating test graphs (complete, random sparse/dense, chordal, bipartite, planar).
To easily identify the tests, I included a naming convention in the script.
I used both the NetworkX library and specific methods.
I implemented the ability to generate graphs within certain node limits and at specified intervals, because depending on the type of graph, I needed different numbers of nodes for the analysis to be as suggestive as possible.

An example : 
```bash
python3 generate_graphs.py --bip 20:40:5
```
Generates bipartite graphs with 20, 25, 30, 35, and 40 nodes.
Multiple commands can be run simultaneously.
The script automatically generates a generated_tests file.

### 3. **`generated_tests`**
Contains the graphs generated based on the project requirements. Each graph is saved in a specific format (*.in) and named according to the graph type (complete, chordal, planar, bipartite, random sparse/dense) to easily identify them when using the runners -> see 4. runners.

### 4. **`runners`**
The folder contains the main scripts for running the tests. These:

- Run the algorithms on the generated test sets.
- Save the results in detailed reports. I have a runner for each algorithm, so I can run them individually for each. 
For some cases, where backtracking had very long times, I implemented various timeouts depending on the available time, after which I no longer run the backtracking -> see the runner for chordal graphs.

### 5. **`reports`**
Contains the reports automatically generated after running the tests. The reports are in Markdown format (*.md), each containing raw data, execution time, and the status of each algorithm in a pretty table format.

### 6. **`generate_graphs**
This folder contains the scripts used to generate the graphs necessary for performance analysis, which are present in the report. -> using the matplotlib library.
Other methods for generating graphs could have been used, but I used this one as it was the method I used in physics labs and it was familiar.


---

## Evaluation
To evaluate the solutions, we need to run the "runners," which run the algorithms on the given tests and generate reports in Markdown format.
Un exemplu de rulare pt bipartite ar fi :

```bash
 python3 runners/run_bip_report.py
```
and this way for each one
