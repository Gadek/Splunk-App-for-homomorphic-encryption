class OperationResult:
    def decrypt(self, HE):
        raise NotImplementedError("Please implement decrypt() method in child class.")

class Operation:
    def encrypt(self, HE):
        raise NotImplementedError("Please implement encrypt() method in child class.")

    def run(self):
        raise NotImplementedError("Please implement run() method in child class.")
