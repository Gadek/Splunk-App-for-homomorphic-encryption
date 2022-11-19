import numpy as np

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils
import sys

class AreStringsPresentInTableOperationResult(OperationResult):
    def __init__(self, result):
        self.result = result
    
    def decrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)
        
        decryptedResult = {}

        for encryptedString in self.result:
            encryptedComparison = self.result[encryptedString]

            decryptedString = Utils.number2string(
                Utils.arrayIntoNumber(
                    HE.decrypt(encryptedString),
                    max_bits
                )
            )
            decryptedComparison = Utils.arrayIntoNumber(
                HE.decrypt(encryptedComparison),
                max_bits
            )

            decryptedResult[decryptedString] = (decryptedComparison == 0)
        
        self.result = decryptedResult

    def __str__(self):
        ret = ''

        for string in self.result:
            comparison = self.result[string]

            ret += string + '\t' + str(comparison) + '\n'
        

        return ret

class AreStringsPresentInTableOperation(Operation):
    def __init__(self, strings = [], table =[]):
        self.strings = strings
        self.table = table
        super().__init__()

    def encrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)
        
        for i in range(len(self.strings)):
            self.strings[i] = HE.encrypt(
                Utils.numberIntoArray(
                    Utils.string2number(self.strings[i]),
                    max_bits
                )
            )
        
        for i in range(len(self.table)):
            self.table[i] = HE.encrypt(
                Utils.numberIntoArray(
                    Utils.string2number(self.table[i]),
                    max_bits
                )
            )

    def run(self) -> AreStringsPresentInTableOperationResult:
        ret = {}

        for s in self.strings:
            comparison = 1

            for t in self.table:
                comparison *= (s - t)
            
            ret[s] = comparison
        
        return AreStringsPresentInTableOperationResult(ret)
