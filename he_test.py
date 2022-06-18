from Pyfhel import Pyfhel
import os

import src.FileIO as FileIO
import src.PyfhelUtils as PyfhelUtils

from src.operations.AddNumbersOperation import AddNumbersOperation
from src.operations.AreStringsPresentInTableOperation import AreStringsPresentInTableOperation

def getHEContext():
    if os.path.exists('HE_context_and_keys'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys')
        return HE

    HE = Pyfhel()
    HE.contextGen(scheme='bfv', n=2**15, t_bits=20)
    HE.keyGen()
    
    PyfhelUtils.saveHE('HE_context_and_keys', HE)

    return HE

HE = getHEContext()

# ===================================
# | Operation example - add numbers |
# ===================================

addNumbersOperation = AddNumbersOperation([127, -2, -2, -2, -1])
addNumbersOperation.encrypt(HE)

FileIO.savePickle('fileA.pickle', addNumbersOperation)

print("Please run processor with input file=fileA.pickle and output file=fileB.pickle")
print("Then press ENTER")
tmp = input()

res = FileIO.loadPickle('fileB.pickle')
res.decrypt(HE)
print(str(res))

# =======================

# =====================================
# | Operation example - string search |
# =====================================

# operation = AreStringsPresentInTableOperation(
#     ["aaa"],
#     [
#         "asd",
#         "gfdgs",
#         "aaa",
#         "123",
#         "f6d",
#     ]
# )
# operation.encrypt(HE)

# FileIO.savePickle('fileA.pickle', operation)

# print("Please run processor with input file=fileA.pickle and output file=fileB.pickle")
# print("Then press ENTER")
# tmp = input()

# res = FileIO.loadPickle('fileB.pickle')

# res.decrypt(HE)
# print(str(res))

# =======================
