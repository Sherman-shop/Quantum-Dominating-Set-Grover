import sys
import os
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Implementation.modular_exponentiation import set_bits, greater_or_eq, add_mod

def test_phase_2():
    print("Testing Phase 2: Modular Logic...")
    
    n = 4
    # Testing Greater Or Eq
    # Case 1: 7 >= 3 ? (Should be 1)
    qr_a = QuantumRegister(n, 'a')
    qr_b = QuantumRegister(n, 'b')
    qr_r = QuantumRegister(1, 'res') # 1 bit result
    qr_aux = QuantumRegister(n*2 + 2, 'aux') # Need plenty of aux
    cr = ClassicalRegister(1, 'c')
    
    qc = QuantumCircuit(qr_a, qr_b, qr_r, qr_aux, cr)
    set_bits(qc, qr_a, 7)
    set_bits(qc, qr_b, 3)
    
    greater_or_eq(qc, qr_a, qr_b, qr_r[0], qr_aux)
    
    qc.measure(qr_r, cr)
    backend = AerSimulator()
    res = backend.run(transpile(qc, backend)).result().get_counts()
    print(f"7 >= 3 Result: {res}")
    
    if list(res.keys())[0] == '1':
        print("✅ Greater/Eq Passed")
    else:
        print("❌ Greater/Eq Failed")

    # Testing Add Mod (Basic)
    # 2 + 3 = 5
    qr_n = QuantumRegister(n, 'n')
    qr_res = QuantumRegister(n, 'sum')
    cr_sum = ClassicalRegister(n, 'c_sum')
    
    qc2 = QuantumCircuit(qr_n, qr_a, qr_b, qr_res, qr_aux, cr_sum)
    set_bits(qc2, qr_a, 2)
    set_bits(qc2, qr_b, 3)
    set_bits(qc2, qr_n, 15) # N is large, so mod shouldn't trigger
    
    add_mod(qc2, qr_n, qr_a, qr_b, qr_res, qr_aux)
    
    qc2.measure(qr_res, cr_sum)
    res2 = backend.run(transpile(qc2, backend)).result().get_counts()
    print(f"2 + 3 (mod 15) Result: {res2}")
    
    if list(res2.keys())[0] == '0101': # 5
        print("✅ Add Mod (Basic) Passed")
    else:
        print("❌ Add Mod Failed")

if __name__ == "__main__":
    test_phase_2()