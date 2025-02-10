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
