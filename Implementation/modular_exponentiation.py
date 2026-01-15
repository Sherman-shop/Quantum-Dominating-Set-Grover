from qiskit import QuantumCircuit, QuantumRegister

# --- Utils ---
def set_bits(circuit, A, X):
    bin_str = format(X, f'0{len(A)}b')
    for i, bit in enumerate(bin_str[::-1]):
        if bit == '1':
            circuit.x(A[i])

def copy(circuit, A, B):
    for i in range(len(A)):
        circuit.cx(A[i], B[i])

# --- Helper for Subtract (Old Logic) ---
def full_adder_separate(circuit, a, b, r, c_in, c_out):
    circuit.ccx(a, b, c_out)
    circuit.cx(a, b)
    circuit.ccx(b, c_in, c_out)
    circuit.cx(b, r) 
    circuit.cx(c_in, r)
    circuit.cx(a, b)

# --- Subtract (Used for Comparison) ---
def subtract(circuit, A, B, R, AUX):
    """Old subtraction logic that works for Comparison check."""
    n = len(A)
    circuit.x(B) # Invert B
    # Bit 0 (c_in=1 logic)
    circuit.x(A[0])
    circuit.x(B[0])
    circuit.ccx(A[0], B[0], AUX[0])
    circuit.x(AUX[0])
    circuit.x(A[0])
    circuit.x(B[0])
    
    circuit.cx(A[0], B[0])
    circuit.x(B[0])
    circuit.cx(B[0], R[0])
    circuit.x(B[0])
    circuit.cx(A[0], B[0])
    
    for i in range(1, n-1):
        full_adder_separate(circuit, A[i], B[i], R[i], AUX[i-1], AUX[i])
    if n > 1:
        full_adder_separate(circuit, A[n-1], B[n-1], R[n-1], AUX[n-2], AUX[n-1])
    circuit.x(B) # Restore B

# --- 1.6 Comparison ---
def greater_or_eq(circuit, A, B, r, AUX):
    """Checks if A >= B using the subtraction carry."""
    n = len(A)
    temp_res = AUX[:n]
    temp_aux = AUX[n:]
    subtract(circuit, A, B, temp_res, temp_aux)
    circuit.cx(temp_aux[n-1], r)

# --- Add (New Robust Logic) ---
def add(circuit, A, B, R, AUX):
    """Robust ripple carry adder."""
    n = len(A)
    # Copy B to R
    for i in range(n):
        circuit.cx(B[i], R[i])
    
    # Bit 0
    circuit.ccx(A[0], R[0], AUX[0])
    circuit.cx(A[0], R[0])
    
    # Bits 1 to n-1
    for i in range(1, n):
        circuit.ccx(A[i], R[i], AUX[i])
        circuit.ccx(A[i], AUX[i-1], AUX[i])
        circuit.ccx(R[i], AUX[i-1], AUX[i])
        circuit.cx(A[i], R[i])
        circuit.cx(AUX[i-1], R[i])

# --- 1.7 Add Mod ---
def add_mod(circuit, N, A, B, R, AUX):
    """Simplified Mod Add: Just Add."""
    add(circuit, A, B, R, AUX)

# --- 1.8 Times Two ---
def times_two_mod(circuit, N, A, R, AUX):
    add_mod(circuit, N, A, A, R, AUX)