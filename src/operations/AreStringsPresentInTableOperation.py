import numpy as np

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils
import sys

class AreStringsPresentInTableOperationResult(OperationResult):
    def __init__(self, result):
        self.result = result
    
    def decrypt(self, HE):
        decryptedResult = {}

        for encryptedString in self.result:
            encryptedComparison = self.result[encryptedString]

            decryptedString = Utils.number2string(
                Utils.getNumberFromSplittedInto15bits(
                    HE.decrypt(encryptedString)
                )
            )
            decryptedComparison = Utils.getNumberFromSplittedInto15bits(
                HE.decrypt(encryptedComparison)
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

    def encrypt(self, HE):
        for i in range(len(self.strings)):
            self.strings[i] = HE.encrypt(
                Utils.splitNumberInto15bits(
                    Utils.string2number(self.strings[i])
                )
            )
        
        for i in range(len(self.table)):
            self.table[i] = HE.encrypt(
                Utils.splitNumberInto15bits(
                    Utils.string2number(self.table[i])
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
