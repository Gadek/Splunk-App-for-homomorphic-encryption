from Pyfhel import Pyfhel
from Naive_Bayes_Classification import NaiveBayes
import numpy as np
import pickle

def init_HE_context(scheme: str):
    if scheme == "bfv":
        HE_context = Pyfhel()

    elif scheme == "ckks":
        n_mults = 8
        HE_context = Pyfhel(context_params={
            'scheme': 'CKKS',
            'n': 2**14,                             
            'scale': 2**30,                         
            # 'qi_sizes': [60]+ [30]*n_mults +[60]
            'qi_sizes': [60, 30, 30, 30, 60]
        })

    else:
        raise Exception("Scheme not recognized")

    return HE_context


def read_context_data():
    # get the public key 
    HE = init_HE_context("bfv")
    HE.load_context("letterbox/mycontext.ctx")
    HE.load_public_key("letterbox/mypk.pk")
    HE.load_relin_key("letterbox/myrlk.rlk")
    HE.load_rotate_key("letterbox/myrotk.rotk")     # needed for Pyfhel.cumul_add() operation

    return HE


if __name__=="__main__":
    # the main flow of the code

    # load the data
    X = np.load("data/X.npy")
    y = np.load("data/y.npy")


    print(X.shape)
    print(y.shape)


    # split the data into train and test sets
    # TODO


    # create the model using X,y data   
    NB = NaiveBayes(X,y)
    NB.fit(X, y)

    # test the data
    # TODO: do it with the test data!!!
    y_pred = NB.predict(X)

    print(sum(y_pred == y)/X.shape[0])
    print(sum(y)/y.shape[0])
    # save the model's mean, covariance and prior for the two classes (spam and not spam)
    NB.save_model("data/model.pickle")

    # receive the data from the client (use the implemented socket functions in the main project)
    input("Please create the necessary files in the letterbox directory and press Enter when ready...")
    client_vect_ctxt = pickle.load(open("letterbox/vect_ctxt.pyfhel", "rb"))

    HE = read_context_data()

    # TODO: implement a funtion in the NaiveBayes class to encrypt the model with the client's public key

    # load the model and run the model
    # NB.load_model( "data/model.pickle" )
    NB.encrypt_the_model(HE)    # ta operacja chyba nie ma sensu - mozemy na spokojnie dodawac plaintext do naszego szyfrogramu pamietajac o uzyciu self.HE.encode()
    result = NB.predict_encrypted(client_vect_ctxt)

    # send the results to the client
    pickle.dump(result, open("letterbox/vect_ctxt.result", "wb"))

