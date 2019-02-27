from copy import deepcopy

import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute

qiskit.IBMQ.load_accounts()
backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))
shots = 100

des_states = {'0', '1', '+x', '-x'}


def check(desierd_state, user_circut, qr, cr):
    circuit = deepcopy(user_circut)
    if '+x' == desierd_state:
        circuit.h(qr)
        desierd_state = '0'
    if '-x' == desierd_state:
        circuit.h(qr)
        desierd_state = '1'

    circuit.measure(qr, cr)
    job = execute(circuit, backend=backend, shots=shots)
    res = job.result().get_counts()

    if desierd_state in res:
        return res[desierd_state] / shots
    else:
        return 0


q = QuantumRegister(1)  # |0>
c = ClassicalRegister(1)

# user interaction 1
circuit = QuantumCircuit(q, c)
circuit.x(q)
print(check('1', circuit, q, c))
print(check('0', circuit, q, c))

# user interaction 2
circuit = QuantumCircuit(q, c)
circuit.h(q)
print(check('+x', circuit, q, c))
print(check('0', circuit, q, c))
