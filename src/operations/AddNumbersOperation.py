import numpy as np

from src.operations.Operation import Operation, OperationResult

class AddNumbersOperationResult(OperationResult):
    def __init__(self, allAdded):
        self.allAdded = allAdded
    
    def decrypt(self, HE):
        self.allAdded = HE.decryptInt(self.allAdded)

    def __str__(self):
        return 'Sum: ' + str(self.allAdded)

class AddNumbersOperation(Operation):
    def __init__(self, numbers = []):
        self.numbers = numbers
    
    def encrypt(self, HE):
        for i in range(len(self.numbers)):
            self.numbers[i] = HE.encryptInt(
                np.array([self.numbers[i]], dtype=np.int64)
            )

    def run(self) -> AddNumbersOperationResult:
        ret = None

        for n in self.numbers:
            if ret is None:
                ret = n
            else:
                ret += n
        
        return AddNumbersOperationResult(ret)
