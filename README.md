# Quantum-Dominating-Set-Grover
# QPROG Project: Quantum Computing Algorithms

This repository contains the implementation of **two Guided Projects** for the Quantum Computing course:
1.  **Project 1**: Implementation of Modular Exponentiation.
2.  **Project 2**: Dominating Set Problem using Grover's Algorithm.

## 📂 Project Structure

### `Implementation/` (Source Code)
-   **Project 1 Files**:
    -   `modular_exponentiation.py`: Contains logic for logic gates, adder, subtractor, comparator, and modular arithmetic.
-   **Project 2 Files**:
    -   `graph.py`: Graph data structure implementation.
    -   `dominating_set.py`: Quantum Oracles for the Dominating Set problem.
    -   `grover.py`: Implementation of Grover's Search Algorithm.

### `Experiments/` (Tests & Results)
-   **Project 1 Scripts**:
    -   `run_project1_experiments.py`: Runs tests for arithmetic logic (Comparison, Addition).
    -   `test_arithmetic.py`: Unit tests for basic adders/subtractors.
    -   **Results**: `p1_exp1_compare.png`, `p1_exp2_add.png`.
-   **Project 2 Scripts**:
    -   `run_experiments.py`: Runs Grover's algorithm on various graph topologies.
    -   **Results**: `exp1_results.png` (Triangle+Isolated), `exp2_results.png`, `exp3_results.png`.

## 🚀 How to Run

**Prerequisites:**
```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib pylatexenc