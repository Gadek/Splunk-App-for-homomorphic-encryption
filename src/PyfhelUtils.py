from Pyfhel import Pyfhel
import os

def saveHE(path, HE):
    if os.path.exists(path):
        print("saveHE: dir already exists!")
        return False
    
    os.mkdir(path)

    HE.save_context(path + "/context")
    HE.save_public_key(path + "/pub.key")
    HE.save_secret_key(path + "/sec.key")
    # HE.save_relin_key(path + "/relin.key")
    # HE.save_rotate_key(path + "/rotate.key")

def loadHE(path):
    HE = Pyfhel()
    
    HE.load_context(path + "/context")
    HE.load_public_key(path + "/pub.key")
    HE.load_secret_key(path + "/sec.key")
    # HE.load_relin_key(path + "/relin.key")
    # HE.load_rotate_key(path + "/rotate.key")

    return HE
