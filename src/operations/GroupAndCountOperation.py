import copy
from functools import reduce
import numpy as np

from Pyfhel import PyCtxt

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils

class GroupAndCountResult(OperationResult):
    def __init__(self, result):
        self.result = result
    
    def decrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)

        decryptedResult = {}

        for data_enc in self.result:
            data_dec = HE.decrypt(data_enc)
            data_dec = data_dec[0]

            if data_dec in decryptedResult:
                continue

            encryptedCount = self.result[data_enc]
            decryptedCountArr = HE.decrypt(encryptedCount)

            count = reduce(lambda a, b: a+b, decryptedCountArr)

            decryptedResult[data_dec] = count
        
        self.result = decryptedResult

    def toLogs(self):
        ret = []

        for d in self.result:
            count = self.result[d]
            ret += [
                'data: {} count: {}\n'.format(str(d), str(count))
            ]
        
        return ret

    def __str__(self):
        ret = ''

        for d in self.result:
            count = self.result[d]

            ret += str(d) + '\t' + str(count) + '\n'
        

        return ret

class GroupAndCountOperation(Operation):
    def __init__(self, data = []):
        self.data = data
        self.__validateData()
        super().__init__()
    
    def __validateData(self):
        if len(self.data) > 180:
            raise Exception("Data can have max 180 elements!")
        
        if len(self.data) < 2:
            raise Exception("Data must have at least 2 elements!")

        for d in self.data:
            if not isinstance(d, int):
                raise Exception("Value must be an int!")
            
            if d > 32767:
                raise Exception("Max value is 32767. Values above are not supported!")
        
            if d < -32768:
                raise Exception("Min value is -32768. Values below are not supported!")

    def encrypt(self, HE):
        self.max_bits = Utils.getHEMaxBits(HE)
        self.he_t = HE.t
        self.zero = HE.encrypt(0)
        self.one = HE.encrypt(1)
        
        for i in range(len(self.data)):
            self.data[i] = HE.encrypt([
                self.data[i]
            ])

    def __applyAttachedContext(self):
        aHE = self.getAttachedHE()

        for i in range(0, len(self.data)):
            self.data[i] = PyCtxt(
                pyfhel=aHE,
                bytestring=self.data[i].to_bytes()
            )
        
        self.zero = PyCtxt(pyfhel=aHE, bytestring=self.zero.to_bytes())
        self.one  = PyCtxt(pyfhel=aHE, bytestring=self.one.to_bytes())
    
    def run(self) -> GroupAndCountResult:
        self.__applyAttachedContext()
        
        counts = {}

        print("Preparing vectors for comparison...")

        dataLen = len(self.data)
        a_enc = copy.copy(self.zero)
        a_ids = []
        b_enc = copy.copy(self.zero)
        b_ids = []

        shift = 0

        for i in range(0, dataLen):
            for j in range(i + 1, dataLen):
                a_ids += [i]
                b_ids += [j]
                a_enc += self.data[i] >> shift
                b_enc += self.data[j] >> shift
                
                shift += 1
        

        print("Checking equality...")
        equalities = Utils.areCtxtsEqual(a_enc, b_enc, self.one, self.he_t)

        print("Masking equalities for each data...")
        for data_id in range(0, dataLen):
            data_enc = self.data[data_id]

            mask = []

            for i in range(len(a_ids)):
                if a_ids[i] == data_id or b_ids[i] == data_id:
                    mask += [1]
                else:
                    mask += [0]
            
            res = equalities * mask + [1]
            counts[data_enc] = res
        
        return GroupAndCountResult(counts)
