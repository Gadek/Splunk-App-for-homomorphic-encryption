import sys
from Pyfhel import Pyfhel, PyCtxt
import numpy as np
import os, math

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

import src.Utils as Utils

from src.operations.Operation import Operation, OperationResult
from src.operations.AddNumbersOperation import AddNumbersOperation
from src.operations.AreStringsPresentInTableOperation import AreStringsPresentInTableOperation
from src.operations.FindMaliciousHashesOperation import FindMaliciousHashesOperation
from src.operations.IpGroupAndCountOperation import IpGroupAndCountOperation
from src.operations.GroupAndCountOperation import GroupAndCountOperation

import pickle

def getHEContext(loadSaveFromFS = True):
    if loadSaveFromFS and os.path.exists('HE_context_and_keys/he_test'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys/he_test')
        return HE

    # Context for Hashes
    # HE = Pyfhel()
    # HE.contextGen(scheme='bfv', n=2**14,  t_bits=17)
    # HE.keyGen()
    # HE.relinKeyGen()

    # Context for grouping
    HE = Pyfhel()
    HE.contextGen(scheme='bfv', n=2**15,  t_bits=17)
    HE.keyGen()
    HE.relinKeyGen()
    HE.rotateKeyGen()
    
    if loadSaveFromFS:
        PyfhelUtils.saveHE('HE_context_and_keys/he_test', HE, True, True)

    return HE

HE = getHEContext(False)
n = HE.get_poly_modulus_degree()
sec = HE.sec
t = HE.t
max_bits = math.floor(math.log2(t / 2 - 1)) # floor was used, since cannot use numbers > t

print(f"n={n}\nsec={sec}\nt={t}\nmax_bits={max_bits}\n")

# ===================================
# | Operation example - add numbers |
# ===================================

# print("=" * 20)
# print("Operation example - add numbers")
# print("-" * 20)

# operation = AddNumbersOperation([127, -2, -2, -2, -1])
# operation.encrypt(HE)
# res = operation.run()
# res.decrypt(HE)

# print(str(res))
# print("-" * 20)

# ===================================
# | Operation example - hash search |
# ===================================

# print("=" * 20)
# print("Operation example - hash search")
# print("-" * 20)

# operation = FindMaliciousHashesOperation([
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492f',
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e',
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e',
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492f',
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e',
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e',
#     '4740284572d290ecbf865e6fa0c63168cff906038db7a2fa7181509360cd3f3b',
#     '4740284572d290ecbf865e6fa0c63168cff906038db7a2fa7181509360c43f3b',
#     '4760284572d290ecbf865e6fa0c63168cff906038db7a2fa7181509360cd3f3b',
# ])
# operation.encrypt(HE)
# res = operation.run()
# res.decrypt(HE)

# print(str(res))
# print("-" * 20)

# =====================================
# | Operation example - group & count |
# =====================================

print("=" * 20)
print("Operation example - group & count")
print("-" * 20)

operation = IpGroupAndCountOperation([
    '10.0.0.156',
    '10.0.0.156',
    '10.0.255.199',
    '10.0.0.156',
    '10.0.255.199',
    '10.0.0.199',
    '10.0.0.199',
])
operation.attachContext(HE)
operation.encrypt(HE)
operationPickled = pickle.dumps(operation)

# Processor
operationOnProcessor = pickle.loads(operationPickled)
res = operationOnProcessor.run()
runnedPickle = pickle.dumps(res)

# Client
resOnClient = pickle.loads(runnedPickle)
resOnClient.decrypt(HE)

print(str(resOnClient))
print("-" * 20)
