from Pyfhel import Pyfhel

class OperationResult:
    def decrypt(self, HE):
        raise NotImplementedError("Please implement decrypt() method in child class.")

class Operation:
    def __init__(self):
        self.__he_attached = None
        self.__he_attached_data = None

    def attachContext(self, HE):
        self.__he_attached_data = {
            'context': HE.to_bytes_context(),
            'public_key': HE.to_bytes_public_key(),
        }

        if not HE.is_relin_key_empty():
            self.__he_attached_data['relin_key'] = HE.to_bytes_relin_key()
        
        if not HE.is_rotate_key_empty():
            self.__he_attached_data['rotate_key'] = HE.to_bytes_rotate_key()
    
    def getAttachedHE(self):
        if self.__he_attached is None:
            if self.__he_attached_data is None:
                return None
            
            self.__he_attached = Pyfhel()
            self.__he_attached.from_bytes_context(self.__he_attached_data['context'])
            self.__he_attached.from_bytes_public_key(self.__he_attached_data['public_key'])
            
            if 'relin_key' in self.__he_attached_data:
                self.__he_attached.from_bytes_relin_key(self.__he_attached_data['relin_key'])
            
            if 'rotate_key' in self.__he_attached_data:
                self.__he_attached.from_bytes_rotate_key(self.__he_attached_data['rotate_key'])
        
        return self.__he_attached
    
    def encrypt(self, HE):
        raise NotImplementedError("Please implement encrypt() method in child class.")
    
    def run(self):
        raise NotImplementedError("Please implement run() method in child class.")
