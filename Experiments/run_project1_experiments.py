import sys
import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Implementation.modular_exponentiation import set_bits, greater_or_eq, add_mod

def save_plot(counts, title, filename):
    # Filter to top 10 to keep it clean
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10])
    fig = plot_histogram(sorted_counts, title=title)
    save_path = os.path.join("Experiments", filename)
    fig.savefig(save_path)
    print(f"Saved plot to: {save_path}")

def run_tests():
    backend = AerSimulator()
    n = 4

    # --- Experiment 1: Comparison (7 >= 3) ---
    print("Running Exp 1: Compare 7 >= 3...")
    qr_a = QuantumRegister(n, 'a')
    qr_b = QuantumRegister(n, 'b')
    qr_r = QuantumRegister(1, 'res')
    qr_aux = QuantumRegister(n*2 + 2, 'aux')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr_a, qr_b, qr_r, qr_aux, cr)
    
    set_bits(qc, qr_a, 7)
    set_bits(qc, qr_b, 3)
    greater_or_eq(qc, qr_a, qr_b, qr_r[0], qr_aux)
    qc.measure(qr_r, cr)
    
    res = backend.run(transpile(qc, backend)).result().get_counts()
    save_plot(res, "Exp1: 7 >= 3 (Expect 1)", "p1_exp1_compare.png")

    # --- Experiment 2: Mod Addition (2 + 3 mod 15) ---
    print("Running Exp 2: Add 2 + 3 mod 15...")
    qr_n = QuantumRegister(n, 'n')
    qr_res = QuantumRegister(n, 'sum') 
    qr_a2 = QuantumRegister(n, 'a2')
    qr_b2 = QuantumRegister(n, 'b2')
    cr_sum = ClassicalRegister(n, 'c_sum')
    
    # Need larger AUX for the robust adder
    # Robust adder needs AUX size = n
    qr_aux2 = QuantumRegister(n + 2, 'aux2')

    qc2 = QuantumCircuit(qr_n, qr_a2, qr_b2, qr_res, qr_aux2, cr_sum)
    set_bits(qc2, qr_a2, 2)
    set_bits(qc2, qr_b2, 3)
    set_bits(qc2, qr_n, 15)
    
    add_mod(qc2, qr_n, qr_a2, qr_b2, qr_res, qr_aux2)
    qc2.measure(qr_res, cr_sum)
    
    res2 = backend.run(transpile(qc2, backend)).result().get_counts()
    save_plot(res2, "Exp2: 2+3 mod 15 (Expect 5)", "p1_exp2_add.png")

if __name__ == "__main__":
    run_tests()