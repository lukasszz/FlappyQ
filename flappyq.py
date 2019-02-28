from copy import deepcopy
from random import randint, shuffle

import qiskit
import numpy as np
from qiskit import Aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute

import qiskit.extensions.standard as gates
from qiskit.tools.visualization import plot_bloch_multivector

levels = {1: {'qubits': 1, 'states': ['0', '1'], 'gates': [gates.x, gates.y, gates.z, gates.iden]},
          2: {'qubits': 2, 'states': ['00', '01', '10', '11'],
              'gates': [gates.x, gates.y, gates.z, gates.iden, gates.h]}}

# qiskit.IBMQ.load_accounts()
backend = Aer.get_backend('qasm_simulator')
shots = 100


def get_desired_state(level):
    states = levels[level]['states']
    shuffle(states)

    return states[0]


def get_random_gates(level):
    gates = levels[level]['gates']
    shuffle(gates)
    target = randint(1, levels[level]['qubits'])
    return (gates[0], target), (gates[1], target)


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
        return res[desierd_state] / shots, read_state(res)
    else:
        return 0, read_state(res)


def read_state(res):
    if 1 == len(res):
        return list(res.keys())[0]

    keys = list(res.keys())
    out = keys[0]
    for k in keys:
        for i in range(len(k)):
            if out[i] != k[i]:
                out = out[:i] + '?' + out[i + 1:]
    return out


def getGoalBlochs(state):
    if state == '00':
        psi = np.array([1,0,0,0])
        return plot_bloch_multivector(psi, title="Goal Qubits")

    elif state == '01':
        psi = np.array([0,1,0,0])
        return plot_bloch_multivector(psi, title="Goal Qubits")

    elif state == '10':
        psi = np.array([0,0,1,0])
        return plot_bloch_multivector(psi, title="Goal Qubits")

    elif state == '11':
        psi = np.array([0,0,0,1])
        return plot_bloch_multivector(psi, title="Goal Qubits")
    elif state == '1':
        psi = np.array([0,1])
        return plot_bloch_multivector(psi, title="Goal Qubits")
    elif state == '0':
        psi = np.array([1,0])
        return plot_bloch_multivector(psi, title="Goal Qubits")

def getCurrentBlochs(psi):
        return plot_bloch_multivector(psi, title="Current Qubits")


if '__main__' == __name__:

    LEVEL = 1
    q = QuantumRegister(levels[LEVEL]['qubits'])  # |0>
    c = ClassicalRegister(levels[LEVEL]['qubits'])
    circuit = QuantumCircuit(q, c)

    desired_state = get_desired_state(LEVEL)
    goal_blochs = getGoalBlochs(desired_state)
    goal_blochs.savefig("desierd_sphere.png")

    print("Desired state is: " + desired_state)

    p = 0.0
    while p < 0.9:
        rgates = get_random_gates(LEVEL)
        gateno = int(input("Select gate [1: " + rgates[0][0].__name__
                           + str(rgates[0][1]) + "] or [2: "
                           + rgates[1][0].__name__ + str(rgates[0][1]) + "] > "))
        gate = rgates[gateno - 1][0]
        target = rgates[gateno - 1][1] - 1
        gate(circuit, q[target])
        p, cstate = check(desired_state, circuit, q, c)
        print("Probabilaty for desired state is: " + str(p))
        print("Current state: |" + cstate + ">")
        cblochs = getGoalBlochs(cstate)
        cblochs.savefig("current_sphere.png")
    print("Success")
