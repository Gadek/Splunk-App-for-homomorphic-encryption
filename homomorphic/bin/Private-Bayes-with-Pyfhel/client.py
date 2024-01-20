from Pyfhel import Pyfhel, PyCtxt
import PyfhelUtils
import os
from generate_vector_mapping import generate_vector
import pickle
import numpy as np
import pandas as pd


def getHEContext():
    # if os.path.exists('HE_context_and_keys'):
    #     HE = PyfhelUtils.loadHE('HE_context_and_keys')
    #     return HE

    HE = Pyfhel()
    # HE.contextGen({"scheme":'bfv', "n":2**13, "t_bits":17, 'sec': 128})
    bfv_params = {"scheme":'bfv', "n":2**14, "t_bits":30}
    HE.contextGen(**bfv_params)
    HE.keyGen()
    
    # PyfhelUtils.saveHE('HE_context_and_keys', HE)

    return HE

def ckks_getHEContext():
    if os.path.exists('HE_context_and_keys'):
        HE = PyfhelUtils.loadHE('HE_context_and_keys')
        return HE   

    n_mults = 8

    HE = Pyfhel(context_params={
    'scheme': 'CKKS',
    'n': 2**14,                             # For CKKS, n/2 values can be encoded in a single ciphertext.
    'scale': 2**30,                         # Each multiplication grows the final scale
    'qi_sizes': [60]+ [30]*n_mults +[60]    # Number of bits of each prime in the chain.
                                            # Intermediate prime sizes should be close to log2(scale).
                                            # One per multiplication! More/higher qi_sizes means bigger
                                            #  ciphertexts and slower ops.
    })

    HE.keyGen()
    
    PyfhelUtils.saveHE('HE_context_and_keys', HE)

    return HE


# Accuracy:
# spam: 4/6
# nonspam: 3/5
# total: 7/11

# email_short = "Subject: collaboration naturally this Short email hard scam on stock collaboration"


if __name__== "__main__":

    # the flow of code: 
    df = pd.read_csv('data/spam_ham_test_dataset.csv')
    size = 5
    # get labels:
    y = df['label_num'][:size]

    # get emails
    X = df['text'][:size]

    # generate HE Context
    HE = getHEContext()
    # generate public and private key (and relinearization key as the multiplication will be performed)
    HE.relinKeyGen()
    HE.rotateKeyGen()

    predictions = []

    for email in X:
        # get the vocabulary from the processor's side (here we just load it from the file) and generate the vector and encrypt it
        vect = generate_vector(email.split())

        # vect_ctxt = np.empty(len(vect), dtype=PyCtxt)

        # for i in range(len(vect)):
        #     vect_ctxt[i] = HE.encrypt(vect[i])

        vect_ctxt = HE.encrypt(vect)    # the length of the whole cipher text is (32768,) (as set in the HE context), but only the length of the vocabulary (120 chars) is what we want to operate on


        # save the public key
        HE.save_public_key("letterbox/mypk.pk")
        HE.save_context("letterbox/mycontext.ctx")
        HE.save_relin_key("letterbox/myrlk.rlk")
        HE.save_rotate_key("letterbox/myrotk.rotk")

        # save the private key (only for debugging!!)
        HE.save_secret_key("letterbox/secret.key")

        # send the generated vector and the public key to the processor
        pickle.dump(vect_ctxt, open("letterbox/vect_ctxt.pyfhel", "wb"))
        # receive the result back
        input("Please do the calculations on the processor and press Enter when ready...")
        result_ctxt = pickle.load(open("letterbox/vect_ctxt.result", "rb"))
        # decrypt (and decode??) the result

        y_pred = [None]*2
        
        for c in range(2):
            probs = HE.decrypt(result_ctxt[0][c])

            # divide the result by the number of classes (2 classes for spam)
            y_pred[c] = np.floor_divide(np.unique([probs]), 2).item() # division not needed as it will not change which one of two values is greater

        # perform the argmax operation on the result (np.argmax(probs, 1))
        decision =  np.argmax(y_pred, 0)

        # if 0 than notspam, if 1 spam

        print(f'Result: {decision} - {"nonspam" if decision == 0 else "spam"}')
        print("Scores: ", y_pred)
        predictions.append(decision)

    print(f"Accuracy: {sum(predictions==y)/X.shape[0]}")

