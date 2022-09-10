import sys
from Pyfhel import Pyfhel
import numpy as np
import os, math

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

import src.Utils as Utils

from src.operations.AddNumbersOperation import AddNumbersOperation
from src.operations.AreStringsPresentInTableOperation import AreStringsPresentInTableOperation
from src.operations.FindMaliciousHashesOperation import FindMaliciousHashesOperation
from src.operations.GroupAndCountOperation import GroupAndCountOperation

def getHEContext(loadSaveFromFS = True):
    if loadSaveFromFS and os.path.exists('HE_context_and_keys'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys')
        return HE

    HE = Pyfhel()
    # HE.contextGen(scheme='bfv', n=2**15,  t_bits=34)
    HE.contextGen(scheme='bfv', n=2**15,  t_bits=17)
    HE.keyGen()
    HE.relinKeyGen()
    HE.rotateKeyGen()
    
    if loadSaveFromFS:
        PyfhelUtils.saveHE('HE_context_and_keys', HE, True, True)

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
#     '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492e'
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

"""
195 => 6
127 => 4
1   => 3
2   => 1
3   => 2
100 => 3
"""
"""
operation = GroupAndCountOperation([
    195,
    195,
    127,
    195,
    127,
    195,
    1,
    195,
    127,
    127,
    195,
    2,
    3,
    100,
    1,
    3,
    1,
    100,
    100,
])
"""

def ip2int(ip):
    ip = ip.split('.')

    if len(ip) > 2:
        raise Exception("Only 2 octets of IP are supported!")

    ret = 0

    for x in ip:
        ret << 8
        ret |= int(x)

    return ret

operation = GroupAndCountOperation([
    ip2int('0.156'),
    ip2int('0.156'),
    ip2int('255.199'),
    ip2int('0.156'),
    ip2int('255.199'),
    ip2int('0.199'),
    ip2int('0.199'),
])
operation.encrypt(HE)
res = operation.run()
res.decrypt(HE)

print(str(res))
print("-" * 20)
