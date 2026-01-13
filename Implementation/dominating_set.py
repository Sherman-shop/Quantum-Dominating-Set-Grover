from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCXGate

def apply_binary_control(qc, register, number, n_bits):
    """Applies X gates to qubits where 'number' has a 0 bit."""
    binary_str = format(number, f'0{n_bits}b')[::-1] 
    for i, bit in enumerate(binary_str):
        if bit == '0':
            qc.x(register[i])

def remove_binary_control(qc, register, number, n_bits):
    apply_binary_control(qc, register, number, n_bits)

def Adj(G, circuit, A, B, b):
    """Sets qubit b to 1 if {number(A), number(B)} is an edge."""
    n_bits = len(A)
    for sublist_idx, neighbors in enumerate(G.adj_list):
        u = sublist_idx
        for v in neighbors:
            if u < v:
                apply_binary_control(circuit, A, u, n_bits)
                apply_binary_control(circuit, B, v, n_bits)
                circuit.mcx(list(A) + list(B), b)
                remove_binary_control(circuit, B, v, n_bits)
                remove_binary_control(circuit, A, u, n_bits)

                apply_binary_control(circuit, A, v, n_bits)
                apply_binary_control(circuit, B, u, n_bits)
                circuit.mcx(list(A) + list(B), b)
                remove_binary_control(circuit, B, u, n_bits)
                remove_binary_control(circuit, A, v, n_bits)

def Dominated(G, circuit, A_list, B, AUX, b):
    """
    Sets b=1 if B is dominated by at least one vertex in A_list.
    """
    n_bits = len(B)
    k = len(A_list)
    
    # Use the first k qubits of AUX as scratch flags for each A_i check
    flags = AUX[:k]
    
    # 1. Compute flags: flags[i] = 1 if (A_i dominates B)
    for i in range(k):
        A_i = A_list[i]
        target_flag = flags[i]
        
        # Check Equality
        for j in range(n_bits):
            circuit.cx(A_i[j], B[j])
            circuit.x(B[j])
        circuit.mcx(list(B), target_flag)
        for j in reversed(range(n_bits)):
            circuit.x(B[j])
            circuit.cx(A_i[j], B[j])
            
        # Check Adjacency
        Adj(G, circuit, A_i, B, target_flag)

    # 2. Compute OR of all flags into b
    # Logic: b = b OR (flags[0] OR flags[1]...)
    # Implementation using De Morgan: b = NOT( AND( NOT flags ) ) assuming b starts at 0.
    
    circuit.x(flags)
    circuit.x(b) 
    
    # If all flags are 0 (so inverted flags are 1), flip b (1 -> 0)
    circuit.mcx(list(flags), b)
    
    # Restore flags state
    circuit.x(flags)
    
    # Crucial Fix: DO NOT apply x(b) here again.
    # Logic Trace:
    # If all flags 0 -> inverted are 1 -> mcx triggers -> b(1) becomes 0. Result: 0. Correct.
    # If any flag 1 -> inverted has 0 -> mcx no trigger -> b(1) stays 1. Result: 1. Correct.
    
    # 3. Uncompute flags
    for i in range(k):
        A_i = A_list[i]
        target_flag = flags[i]
        Adj(G, circuit, A_i, B, target_flag)
        for j in range(n_bits):
            circuit.cx(A_i[j], B[j])
            circuit.x(B[j])
        circuit.mcx(list(B), target_flag)
        for j in reversed(range(n_bits)):
            circuit.x(B[j])
            circuit.cx(A_i[j], B[j])

def AllDominated(G, circuit, A_list, AUX, b):
    """
    Sets b to 1 if every vertex v in G is dominated by A_list.
    """
    n = G.n
    n_bits_node = len(A_list[0])
    
    B_temp = AUX[0:n_bits_node]
    flags = AUX[n_bits_node : n_bits_node + n]
    inner_aux = AUX[n_bits_node + n:]
    
    # 1. Loop through all vertices v and compute their dominated status
    for v in range(n):
        v_bin = format(v, f'0{n_bits_node}b')[::-1]
        for i, bit in enumerate(v_bin):
            if bit == '1':
                circuit.x(B_temp[i])
        
        Dominated(G, circuit, A_list, B_temp, inner_aux, flags[v])
        
        for i, bit in enumerate(v_bin):
            if bit == '1':
                circuit.x(B_temp[i])
                
    # 2. Check if ALL flags are 1 (AND logic)
    circuit.mcx(list(flags), b)
    
    # 3. Uncompute everything
    for v in reversed(range(n)):
        v_bin = format(v, f'0{n_bits_node}b')[::-1]
        for i, bit in enumerate(v_bin):
            if bit == '1':
                circuit.x(B_temp[i])
        
        Dominated(G, circuit, A_list, B_temp, inner_aux, flags[v])
        
        for i, bit in enumerate(v_bin):
            if bit == '1':
                circuit.x(B_temp[i])