import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute

qiskit.IBMQ.load_accounts()
backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))
shots = 100


def check(desierd_state, counts, shots):
    if desierd_state in counts:
        return st[desierd_state] / shots
    else:
        return 0


q = QuantumRegister(2)  # |0>
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

# user interaction
qc.x(q[1])

# copy and measure
qc.measure(q, c)
job = execute(qc, backend=backend, shots=shots)
result = job.result()
st = result.get_counts()

# check
print(st)
print(check('00', st, shots))
print(check('10', st, shots))
print(check('11', st, shots))
