import numpy as np

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils
import sys

class FindMaliciousHashesResult(OperationResult):
    def __init__(self, result):
        self.result = result
    
    def decrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)

        decryptedResult = {}

        for encryptedHash in self.result:
            encryptedComparison = self.result[encryptedHash]

            decryptedHash = Utils.number2hash(
                Utils.arrayIntoNumber(
                    HE.decrypt(encryptedHash),
                    max_bits
                )
            )
            decryptedComparison = Utils.arrayIntoNumber(
                HE.decrypt(encryptedComparison),
                max_bits
            )

            decryptedResult[decryptedHash] = (decryptedComparison == 0)
        
        self.result = decryptedResult

    def toLogs(self):
        ret = []

        for hash in self.result:
            comparison = self.result[hash]
            ret += [
                'hash: {} is malicious?: {}\n'.format(hash, str(comparison))
            ]
        
        return ret

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
        max_bits = Utils.getHEMaxBits(HE)
        
        for i in range(len(self.hashes)):
            self.hashes[i] = HE.encrypt(
                Utils.numberIntoArray(
                    Utils.hash2number(self.hashes[i]),
                    max_bits
                )
            )
        
        for i in range(len(self.malicious)):
            self.malicious[i] = HE.encrypt(
                Utils.numberIntoArray(
                    Utils.hash2number(self.malicious[i]),
                    max_bits
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
