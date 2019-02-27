from copy import deepcopy
from random import randint

import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute

from qiskit.extensions.standard.x import x as gate_x

qiskit.IBMQ.load_accounts()
backend = qiskit.providers.ibmq.least_busy(qiskit.IBMQ.backends(simulator=True))
shots = 100


def get_desired_state():
    # des_states = {'0', '1', '+x', '-x'}
    states = ['0', '1']
    selection = randint(0, len(states) - 1)

    return states[selection]


def get_random_gate():
    import qiskit.extensions.standard as gates
    gates = [gates.x, gates.y, gates.z, gates.iden]
    selection = randint(0, len(gates) - 1)
    return gates[selection]


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
    print(res)
    if desierd_state in res:
        return res[desierd_state] / shots
    else:
        return 0


q = QuantumRegister(1)  # |0>
c = ClassicalRegister(1)
circuit = QuantumCircuit(q, c)

desired_state = get_desired_state()
print("Desired state is: " + desired_state)

p = 0.0
while p < 0.9:
    rgate = [get_random_gate(), get_random_gate()]
    gateno = int(input("Select gate [1: " + rgate[0].__name__
                       + "] or [2: " + rgate[1].__name__ + "] > "))

    rgate[gateno - 1](circuit, q)
    p = check(desired_state, circuit, q, c)
    print("Probabilaty for desired state is: " + str(p))

print("Success")