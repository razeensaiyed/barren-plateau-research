import qiskit
import qiskit_aer
import cirq

print("Qiskit version:", qiskit.__version__)
print("Qiskit Aer version:", qiskit_aer.__version__)
print("Cirq version:", cirq.__version__)

# Tiny Bell-state circuit in Qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sim = AerSimulator()
result = sim.run(qc, shots=100).result()
print("Qiskit Bell state counts:", result.get_counts())

# Same Bell-state circuit in Cirq
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key="result"),
)
cirq_sim = cirq.Simulator()
cirq_result = cirq_sim.run(circuit, repetitions=100)
print("Cirq Bell state counts:", cirq_result.histogram(key="result"))