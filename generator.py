from qiskit import Aer, ClassicalRegister, execute, QuantumCircuit, QuantumRegister
from qiskit.tools.monitor import job_monitor



def qrandint(min, max):
    range = max - min
    qaddend = range * qmeasure('sim')
    qsum = qaddend + min
    qint = int(qsum +.5)
    return qint

def qqrandint(min, max):
    range = max - min
    qaddend = range * qmeasure('real')
    qsum = qaddend + min
    qint = int(qsum +.5)
    return qint

def quniform(min, max):
    range = max - min
    qaddend = range * qmeasure('sim')
    qsum = qaddend + min
    return qsum

def qquniform(min, max):
    range = max - min
    qaddend = range * qmeasure('real')
    qsum = qaddend + min
    return qsum

def qmeasure(hardware):
    if (hardware == 'real'):
        qubits = 14
        provider = IBMQ.get_provider(hub='ibm-q')
        provider.backends()
        backend = provider.get_backend('ibmq_16_melbourne')
    else:
        qubits = 32
        backend = Aer.get_backend('qasm_simulator')
        
    q = QuantumRegister(qubits) # initialize all available quantum registers (qubits)
    c = ClassicalRegister(qubits) # initialize classical registers to measure the qubits
    qc = QuantumCircuit(q, c) # initialize the circuit

    i = 0
    while i < qubits:
        qc.h(q[i]) # put all qubits into superposition states so that each will measure as a 0 or 1 completely at random
        i = i + 1
   
    qc.measure(q, c) # collapse the superpositions and get random zeroes and ones
    job = execute(qc, backend, shots=1)
    job_monitor(job)
    result = job.result()
    mraw = result.get_counts(qc)
    m = str(mraw)
    subtotal = 0
    for i in range(qubits):
        subtotal = subtotal + (int(m[i+2]) * 2**(i)) # convert each binary digit to its decimal value, but read left-to-right for simplicity
    multiplier = subtotal / (2**qubits) # convert the measurement to a value between 0 and 1
    return multiplier

print(qrandint(-100, 100))
print(quniform(-1, 1))
print(qqrandint(-100, 100))
print(qquniform(-1, 1))
