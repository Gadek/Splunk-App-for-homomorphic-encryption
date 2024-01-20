import numpy as np

from src.operations.Operation import Operation, OperationResult
import src.Utils as Utils
import sys

class FindMaliciousHashesResult(OperationResult):
    def __init__(self, result, numberOfHashes):
        self.result = result
        self.numberOfHashes = numberOfHashes
    
    def decrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)
        
        numberOfHashes = Utils.arrayIntoNumber(
            HE.decrypt(self.numberOfHashes),
            max_bits
        )

        decryptedResult = {}

        for encryptedBatchOfHashes in self.result:
            hashesEncoded = Utils.numbersFromBatch(
                HE.decrypt(encryptedBatchOfHashes),
                HE
            )

            hashesDecoded = []

            for h in hashesEncoded:
                tmp_hash = Utils.number2hash(
                    Utils.arrayIntoNumber(
                        h,
                        max_bits
                    )
                )

                hashesDecoded += [tmp_hash]
            
            # COMPARISONS
            encryptedBatchOfComparisons = self.result[encryptedBatchOfHashes]
            comparisonsEncoded = Utils.numbersFromBatch(
                HE.decrypt(encryptedBatchOfComparisons),
                HE
            )
            
            comparisonsDecoded = []

            for comp in comparisonsEncoded:
                tmp_comp = Utils.arrayIntoNumber(
                    comp,
                    max_bits
                )

                comparisonsDecoded += [tmp_comp]

            for i in range(min(
                len(hashesDecoded),
                len(comparisonsDecoded),
                numberOfHashes
            )):
                h = hashesDecoded[i]
                c = comparisonsDecoded[i]

                decryptedResult[h] = (c == 0)
        
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
        super().__init__()

    def encrypt(self, HE):
        self.max_bits = Utils.getHEMaxBits(HE)
        self.n = HE.n
        self.one = HE.encrypt(1)

        self.numberOfHashes = HE.encrypt(
            Utils.numberIntoArray(
                len(self.hashes),
                self.max_bits
            )
        )
        
        for i in range(len(self.hashes)):
            self.hashes[i] = Utils.numberIntoArray(
                Utils.hash2number(self.hashes[i]),
                self.max_bits
            )
        
        self.hashes = Utils.batchNumbers(self.hashes, HE)

        for i in range(len(self.hashes)):
            self.hashes[i] = HE.encrypt(
                self.hashes[i]
            )
    
    def __loadMaliciousHashes(self):
        self.malicious = []

        if self.max_bits is None:
            print("Error: max_bits is not set!")
            return
        
        if self.n is None:
            print("Error: n is not set!")
            return
        
        with open("malicious hashes.txt") as f:
            for line in f:
                h = line.strip()

                self.malicious += [
                    Utils.repeatNumber(
                        Utils.numberIntoArray(
                            Utils.hash2number(h),
                            self.max_bits
                        ),
                        self.max_bits,
                        self.n
                    )
                ]

    def run(self) -> FindMaliciousHashesResult:
        ret = {}

        if self.malicious is None:
            self.__loadMaliciousHashes()
        
        for s in self.hashes:
            comparisons = []

            for t in self.malicious:
                comp = (s - t)
                ~comp
                comparisons += [comp]
            
            while len(comparisons) > 1:
                tmpComparisons = []

                for i in range(0, len(comparisons), 2):
                    j = i + 1
                    
                    if j >= len(comparisons):
                        # last one is left - just copy it
                        tmpComparisons += [comparisons[i]]
                        break

                    tmpComp = comparisons[i] * comparisons[j]
                    ~tmpComp
                    tmpComparisons += [tmpComp]
                
                comparisons = tmpComparisons
            
            ret[s] = comparisons[0]
        
        return FindMaliciousHashesResult(ret, self.numberOfHashes)
