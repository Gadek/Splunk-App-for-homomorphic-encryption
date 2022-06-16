import numpy as np

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils
import sys

class FindMaliciousHashesResult(OperationResult):
    def __init__(self, result):
        self.result = result
    
    def decrypt(self, HE):
        decryptedResult = {}

        for encryptedHash in self.result:
            encryptedComparison = self.result[encryptedHash]

            decryptedHash = Utils.number2hash(
                Utils.getNumberFromSplittedInto15bits(
                    HE.decrypt(encryptedHash)
                )
            )
            decryptedComparison = Utils.getNumberFromSplittedInto15bits(
                HE.decrypt(encryptedComparison)
            )

            decryptedResult[decryptedHash] = (decryptedComparison == 0)
        
        self.result = decryptedResult

    def __str__(self):
        ret = ''

        for hash in self.result:
            comparison = self.result[hash]

            ret += hash + '\t' + str(comparison) + '\n'
        

        return ret

class FindMaliciousHashesOperation(Operation):
    def __init__(self, hashes = [], malicious =[]):
        self.hashes = hashes
        self.malicious = malicious

    def encrypt(self, HE):
        for i in range(len(self.hashes)):
            self.hashes[i] = HE.encrypt(
                Utils.splitNumberInto15bits(
                    Utils.hash2number(self.hashes[i])
                )
            )
        
        for i in range(len(self.malicious)):
            self.malicious[i] = HE.encrypt(
                Utils.splitNumberInto15bits(
                    Utils.hash2number(self.malicious[i])
                )
            )

    def run(self) -> FindMaliciousHashesResult:
        ret = {}

        for s in self.hashes:
            comparison = 1

            for t in self.malicious:
                comparison *= (s - t)
            
            ret[s] = comparison
        
        return FindMaliciousHashesResult(ret)
