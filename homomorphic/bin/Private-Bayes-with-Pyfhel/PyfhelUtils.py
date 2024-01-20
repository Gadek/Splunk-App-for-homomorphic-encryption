from Pyfhel import Pyfhel
import os

def saveHE(path, HE, withRelinKey = False, withRotateKey = False):
    if os.path.exists(path):
        print("saveHE: dir already exists!")
        return False
    
    os.makedirs(path, exist_ok=True)

    HE.save_context(path + "/context")
    HE.save_public_key(path + "/pub.key")
    HE.save_secret_key(path + "/sec.key")
    
    if withRelinKey:
        HE.save_relin_key(path + "/relin.key")
    
    if withRotateKey:
        HE.save_rotate_key(path + "/rotate.key")

def loadHE(path):
    HE = Pyfhel()
    
    HE.load_context(path + "/context")
    HE.load_public_key(path + "/pub.key")
    HE.load_secret_key(path + "/sec.key")

    # relin key
    relinKeyPath = path + "/relin.key"
    
    if os.path.exists(relinKeyPath):
        HE.load_relin_key(relinKeyPath)

    # rotate key
    rotateKeyPath = path + "/rotate.key"
    
    if os.path.exists(rotateKeyPath):
        HE.load_rotate_key(rotateKeyPath)

    return HE