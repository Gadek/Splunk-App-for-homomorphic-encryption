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
], [
    '11ba3e87ec5e20a2d41063696b27ece12d644bd32892f33464d5d62ca9be492f',
    '90d4afcf348556a0b201ebff84e56f269bf4af675e755948a44aa592e09dc2e5',
    '06d076133e081626ecce85cd1f4c7bf89e21ea346de5122ca38234944f68a1ea',
    'a9a6d795c575475c55fbd0426d062390d366fb6f62c3c6dba7ffedf632fcbb2c',
    '7379d0e904c6ba03da23b99a6190127cfcac925e1d29c39f7a3e8a73953c943e',
    '175628a86e6e111b97feb4af3551a7fd4e5765dfea1764b155bb9817f1757ae4',
    '83f035395413f9f7fd4f5594c9967f9fc09c8f5ed35c43005f9d1c7fe94b0160',
    'a2635db95253f39d746f6c4eaa91be0c6bbec6ab577391df1131aa5542db857e',
    '86fa730e9910130312cbea36ba541daf06712523465db99a33d83d6f96bdfb62',
    '4740284572d290ecbf865e6fa0c63168cff906038db7a2fa7181509360cd3f3b',
    'bade5566650c42fa6f920db80f112ea974631c0dfe28d5a837e223ab85c5788e',
    '29ca6567cae5faed6e0f2e74869cdd50d605d6e1cd08235d24c853a6d279a57d',
    '68539cf33fca5879a9ae9634e31fe1ca03c7a31577cf47654da6560f50b0f5d5',
    'd08ae696a91a588379d5d1b184f90cc26ae1d8ef52ad015c83ae2aa7e8f1a3ff',
])
operation.encrypt(HE)
res = operation.run()
res.decrypt(HE)

print(str(res))
print("-" * 20)
