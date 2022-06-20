from Pyfhel import Pyfhel
import numpy as np
import os, math

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

from src.operations.AddNumbersOperation import AddNumbersOperation
from src.operations.AreStringsPresentInTableOperation import AreStringsPresentInTableOperation
from src.operations.FindMaliciousHashesOperation import FindMaliciousHashesOperation

def getHEContext(loadSaveFromFS = True):
    if loadSaveFromFS and os.path.exists('HE_context_and_keys'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys')
        return HE

    HE = Pyfhel()
    HE.contextGen(scheme='bfv', n=2**15,  t_bits=34)
    HE.keyGen()
    
    if loadSaveFromFS:
        PyfhelUtils.saveHE('HE_context_and_keys', HE)

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

print("=" * 20)
print("Operation example - add numbers")
print("-" * 20)

operation = AddNumbersOperation([127, -2, -2, -2, -1])
operation.encrypt(HE)
res = operation.run()
res.decrypt(HE)

print(str(res))
print("-" * 20)

# ===================================
# | Operation example - hash search |
# ===================================

print("=" * 20)
print("Operation example - hash search")
print("-" * 20)

operation = FindMaliciousHashesOperation([
    '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492f',
    '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e'
])
operation.encrypt(HE)
res = operation.run()
res.decrypt(HE)

print(str(res))
print("-" * 20)
