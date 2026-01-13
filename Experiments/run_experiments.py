import sys
import os
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Add the parent directory to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Implementation.graph import Graph
from Implementation.grover import run_grover

def save_plot(counts, title, filename):
    """Generates and saves a histogram of the results."""
    # Filter counts to keep only the top 10 to make chart readable
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10])
    
    fig = plot_histogram(sorted_counts, title=title)
    save_path = os.path.join("Experiments", filename)
    fig.savefig(save_path)
    print(f"Saved plot to: {save_path}")

def experiment_1_triangle_isolated():
    """
    Experiment 1: Triangle (0,1,2) + Isolated (3).
    Looking for Dominating Set of size 2.
    Solution: Must include 3, and one of {0,1,2}.
    """
    print("\n--- Running Experiment 1: Triangle + Isolated Node ---")
    g = Graph()
    g.set_number_vertices(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(0, 2)
    # Node 3 is isolated (no edges added)
    
    counts, _ = run_grover(g, k=2, iterations=1)
    save_plot(counts, "Exp1: Triangle+Isolated (k=2)", "exp1_results.png")

def experiment_2_linear_graph():
    """
    Experiment 2: Linear Path 0-1-2-3.
    Looking for Dominating Set of size 2.
    Solutions: {1,2}, {0,2}, {0,3}?? 
    Let's see what Quantum finds.
    """
    print("\n--- Running Experiment 2: Linear Path 0-1-2-3 ---")
    g = Graph()
    g.set_number_vertices(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    
    counts, _ = run_grover(g, k=2, iterations=1)
    save_plot(counts, "Exp2: Line Graph 4 Nodes (k=2)", "exp2_results.png")

def experiment_3_impossible_case():
    """
    Experiment 3: Square Graph 0-1-2-3 (Cycle).
    Looking for Dominating Set of size 1. (Impossible, needs at least 2)
    We expect no clear peak (noise).
    """
    print("\n--- Running Experiment 3: Square Cycle (Impossible k=1) ---")
    g = Graph()
    g.set_number_vertices(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    
    counts, _ = run_grover(g, k=1)
    save_plot(counts, "Exp3: Square Cycle (k=1, Impossible)", "exp3_results.png")

if __name__ == "__main__":
    # Ensure the directory exists
    if not os.path.exists("Experiments"):
        os.makedirs("Experiments")
        
    experiment_1_triangle_isolated()
    experiment_2_linear_graph()
    experiment_3_impossible_case()
    
    print("\nAll experiments completed! Check the 'Experiments' folder.")