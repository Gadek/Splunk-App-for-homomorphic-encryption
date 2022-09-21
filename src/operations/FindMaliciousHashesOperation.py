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
                '{},{}\n'.format(hash, str(comparison))
            ]
        
        return ret

    def __str__(self):
        ret = ''

        for hash in self.result:
            comparison = self.result[hash]

            ret += hash + '\t' + str(comparison) + '\n'
        

        return ret

class FindMaliciousHashesOperation(Operation):
    def __init__(self, hashes = []):
        self.hashes = hashes
        self.malicious = None
        self.max_bits = None

    def encrypt(self, HE):
        self.max_bits = Utils.getHEMaxBits(HE)
        
        for i in range(len(self.hashes)):
            self.hashes[i] = HE.encrypt(
                Utils.numberIntoArray(
                    Utils.hash2number(self.hashes[i]),
                    self.max_bits
                )
            )
    
    def __loadMaliciousHashes(self):
        self.malicious = []

        if self.max_bits is None:
            print("Error: max_bits is not set!")
            return
        
        with open("malicious hashes.txt") as f:
            for line in f:
                self.malicious += [
                    Utils.numberIntoArray(
                        Utils.hash2number(line[:-1]),
                        self.max_bits
                    )
                ]

    def run(self) -> FindMaliciousHashesResult:
        ret = {}

        if self.malicious is None:
            self.__loadMaliciousHashes()

        for s in self.hashes:
            comparison = 1

            for t in self.malicious:
                comparison *= (s - t)

            ret[s] = comparison
        
        return FindMaliciousHashesResult(ret)
