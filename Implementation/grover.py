from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# 导入我们之前写的模块
try:
    # 模式 A: 当作为外部脚本被调用时 (例如从 Experiments 运行)
    from Implementation.graph import Graph
    from Implementation.dominating_set import AllDominated
except ImportError:
    # 模式 B: 当直接运行时 (例如直接跑 grover.py)
    from graph import Graph
    from dominating_set import AllDominated

def diffuser(n_qubits):
    """
    Grover's Diffuser (Inversion about the mean).
    It amplifies the probability of the marked states.
    """
    qc = QuantumCircuit(n_qubits)
    # Apply H gates to all qubits
    qc.h(range(n_qubits))
    # Apply X gates to all qubits
    qc.x(range(n_qubits))
    
    # Apply Multi-Controlled Z (MCZ)
    # Equivalent to: H(last) -> MCX -> H(last)
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    
    # Apply X gates
    qc.x(range(n_qubits))
    # Apply H gates
    qc.h(range(n_qubits))
    
    # Convert to gate
    gate = qc.to_gate()
    gate.name = "Diffuser"
    return gate

def run_grover(graph, k, iterations=None):
    """
    Runs Grover's algorithm to find a Dominating Set of size k.
    """
    n = graph.n
    # Number of bits to represent one node index
    # e.g., for 4 nodes, we need 2 bits (00, 01, 10, 11)
    n_bits_node = int(np.ceil(np.log2(n)))
    
    # Total input qubits: k nodes * n_bits_node per node
    # e.g., finding a set of size 2 in a 4-node graph: 2 * 2 = 4 qubits.
    num_input_qubits = k * n_bits_node
    
    # Auxiliary qubits needed for the Oracle
    # We need enough scratch space for the 'AllDominated' check.
    # From previous logic: we need at least n_bits_node + extra for comparisons.
    # Let's allocate a generous amount to be safe (simulators can handle it).
    num_aux_qubits = n_bits_node + 2 + n  
    
    # Output qubit for the Oracle (the one that gets flipped)
    num_target_qubit = 1
    
    # Total qubits
    total_qubits = num_input_qubits + num_aux_qubits + num_target_qubit
    
    # Registers
    qr_input = QuantumRegister(num_input_qubits, 'input')
    qr_aux = QuantumRegister(num_aux_qubits, 'aux')
    qr_target = QuantumRegister(num_target_qubit, 'target')
    cr = ClassicalRegister(num_input_qubits, 'meas')
    
    qc = QuantumCircuit(qr_input, qr_aux, qr_target, cr)
    
    # 1. Initialization (Superposition)
    qc.h(qr_input)
    
    # Initialize target qubit to |-> state (Eigenstate of X)
    qc.x(qr_target)
    qc.h(qr_target)
    
    # 2. Determine iterations (if not provided, use optimal ~sqrt(N))
    if iterations is None:
        N = 2**num_input_qubits
        iterations = int(np.floor((np.pi / 4) * np.sqrt(N)))
        # For small cases, usually 1 or 2 is enough.
        # print(f"Auto-calculated iterations: {iterations}")

    # 3. Grover Loop
    for _ in range(iterations):
        # -- Oracle --
        # We need to slice the input register into k chunks (A_1, A_2 ... A_k)
        A_list = []
        for i in range(k):
            # Slicing the input register
            start = i * n_bits_node
            end = (i + 1) * n_bits_node
            A_list.append(qr_input[start:end])
            
        # Apply the Verifier (Oracle)
        # Note: AllDominated expects (G, circuit, A_list, AUX, b)
        AllDominated(graph, qc, A_list, qr_aux, qr_target[0])
        
        # -- Diffuser --
        qc.append(diffuser(num_input_qubits), qr_input)
        
    # 4. Measurement
    qc.measure(qr_input, cr)
    
    # 5. Simulation
    backend = AerSimulator()
    # Transpile for the simulator
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=1024).result()
    counts = result.get_counts()
    
    return counts, qc

# 简易测试代码 (Run this to verify)
if __name__ == "__main__":
    # Create a simple triangle graph (0-1, 1-2, 2-0) + isolated 3
    # 0 -- 1
    # |  /
    # 2    3
    # Dominating set of size 2 should be {1, 3} or {0, 3} etc.
    g = Graph()
    g.set_number_vertices(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(0, 2)
    
    print("Running Grover on a 4-node graph, looking for Dominating Set of size k=2...")
    counts, _ = run_grover(g, k=2)
    
    print("\nTop 5 Results:")
    # Sort by frequency
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for bitstring, count in sorted_counts[:5]:
        # Convert bitstring to node indices
        # Bitstring is e.g. "1101" -> Node 3 (11) and Node 1 (01)
        # Be careful with Endianness: Qiskit returns bits reversed usually?
        # Actually Qiskit counts are key string.
        # Let's just print raw first.
        print(f"State: {bitstring} | Count: {count}")
    
    print("\n[System Check]: If you see counts appearing, the Engine is running!")