# data
# what type of data can we use?
# 1. emails where the spam filrtering will be performed (problem: need to add grouping and counting functionality on encrypted data which not trivial) -> think of possible ways to circumvent that
# 2. for DDOS detection - what kind of data?? some kind of vector with information about the attack happenning ??

# alternative: linear regression
# 1. DDOS data detection - a vector with for eg. packet statistics


# Plan
# 1. build vocabulary from the email dataset (the code is not important - just the resulting vocabulary.txt file can be present in the final repo)
# 2. encode the email into the vector with vocabulary words as indexes (in the final fhe implementation it should be done on the client side)
# 3. send the encoded vector to the processor
# 4. the processor runs the received vector against its model (verify if this is not too resource intensive)

"""
# data descritpion (for the file emails_small.csv)
(Pdb) type(data)
<class 'pandas.core.frame.DataFrame'>
(Pdb) data.shape
(98, 2)                     # pd.Datraframe 98 emails with two labels - spam or non-spam
(Pdb) len(vocabulary)
37441                       # the vocabulary -> all the words contained in the emails.csv file 
# (Pdb) type(X)
<class 'numpy.ndarray'>
(Pdb) X.shape
(98, 37441)
(Pdb) type(y)
<class 'numpy.ndarray'>
(Pdb) y.shape
(98,)
(Pdb) 

"""


"""
Resources:
https://github.com/aladdinpersson/Machine-Learning-Collection/tree/master/ML/Projects/spam_classifier_naive_bayes 

"""


import numpy as np
import pickle
from typing import Optional
from Pyfhel import Pyfhel, PyCtxt
from Utils import ctxt_to_power
from decimal import *


class NaiveBayes:
    """
    A class implementing Naive Bayes algorithm for e-mail spam classification:

    Formula:

    P(H|e) = P(e|H)*P(H) / P(e)
    where
    H - hipothesis
    e - evidence
    """
    def __init__(self, X: np.ndarray, y: Optional[np.ndarray]=None) -> None:
        """
        @params:
            X - a numpy 2D array containing all emails mapped into a vector of words' occurances from the vocabulary (training set)
            y - the spam/nonspam labels to the X data
        """
        self.num_examples, self.num_features = X.shape     # (number of emails, number of words in the vocabulary)
        self.eps = 1e-6
        self.num_classes = len(np.unique(y))        # for spam/nonspam classification self.num_classes = 2


    def fit(self, X, y):
        """The training method
        @params:
            X:  
            y: 
        """
        assert X.shape[0] == y.shape[0], "No classes provided. Only prediction is possible"      # TODO: can we globally "block" execution of a certain function without everytime checking whether y is not None and raising Exception

        self.classes_mean = {}
        self.classes_variance = {}
        self.classes_prior = {}

        for c in range(self.num_classes):
            X_c = X[y == c]
            self.classes_mean[str(c)] = np.mean(X_c, axis=0, dtype=np.int64)        # changing type to , dtype=np.int64 as BFV requires integers only
            self.classes_variance[str(c)] = np.var(X_c, axis=0, dtype=np.float64)
            self.classes_prior[str(c)] = np.float64(X_c.shape[0] / X.shape[0])


    def predict(self, X):
        """
        This function will be run when FHE encrypted!!!
        """
        probs = np.zeros((self.num_examples, self.num_classes))

        for c in range(self.num_classes):
            prior = self.classes_prior[str(c)]
            probs_c = self.density_function(
                X, self.classes_mean[str(c)], self.classes_variance[str(c)]
            )
            probs[:, c] = probs_c + np.log(prior)

        # when encrypted just return probs and let the client run the argmax

        return np.argmax(probs, 1)


    def predict_encrypted(self, X):
        """
        This function will be run when FHE encrypted!!!
        """
        # FIXME: beacuase we are not training and only predicting from one sample the shape is not (self.num_examples, self.num_classes) but (1, self.num_classes)
        probs_ctxt = np.zeros((1, self.num_classes), dtype=PyCtxt)
        for c in range(self.num_classes):
            # prior = self.classes_prior_ctxt[c]
            prior_log = self.classes_prior_log_ctxt[c]
            probs_c = self.density_function_encrypted(X, self.classes_mean[str(c)], self.classes_variance[str(c)])        # we don't actually have to encrypt the mean and variance
            probs_ctxt[:, c] = probs_c + self.HE.encode(self.classes_prior[str(c)])

            # probs_ctxt[c] = probs_c[c] + prior_log

        # when encrypted just return probs and let the client run the argmax 
        return probs_ctxt


    def density_function(self, x, mean, sigma):
        """Supposedly a method implementing the Gaussian probablility distribution
        Used to calculate probability for NB (Gaussian Naive Bayes -> normal distribution).
        Parameters to the Gaussian function can be modified to obtain better results.
        """
        # TODO: check implementation and rewrite if possible
        const = -self.num_features / 2 * np.log(2 * np.pi) - 0.5 * np.sum(
            np.log(sigma + self.eps)
        )
        probs = 0.5 * np.sum(np.power(x - mean, 2) / (sigma + self.eps), 1)     
        ''' # FIXME: potential error: during training we get the x which shape is (num_emails, num_features)
        when predicting class for one email thee shape is (num_features,) and thus we should np.sum it on the axis=0 not axis=1
        '''
        return const - probs

    def density_function_encrypted(self, x, mean, sigma):
        """Supposedly a method implementing the Gaussian probablility distribution
        Used to calculate probability for NB (Gaussian Naive Bayes -> normal distribution).
        Parameters to the Gaussian function can be modified to obtain better results.
        """
        divisor = sigma + self.eps      # TODO: verify float to int conversion

        x = self.HE.square(x - self.HE.encode(mean), in_new_ctxt=True)


        x *= self.HE.encode((1 / divisor).astype(np.int64))

        self.HE.relinearize(x)  # cumul_add requires ctxt of size 2
        x_sum = self.HE.cumul_add(x)

        # calculate the constant
        const = -self.num_features / 2 * np.log(2 * np.pi) - 0.5 * np.sum(np.log(sigma+ self.eps))
        return self.HE.encrypt(2*const) - x_sum     # use self.HE.encrypt NOT encode as subtracting plaintext - ctxt is not supported

    def save_model(self, path):
        model = {"mean": self.classes_mean, "variance": self.classes_variance, "prior": self.classes_prior}
        pickle.dump( model, open(path, "wb") )


    def load_model(self, path):
        """ Load functionality is not used right now. """
        model = pickle.load(open(path, "rb"))
        self.classes_mean = model["mean"]
        self.classes_var = model["variance"]
        self.classes_prior = model["prior"]


    def encrypt_the_model(self, HE):
        # TODO: encrypt the model data with the user provided public key
        # TODO: rewrite this function as "TypeError: <Pyfhel ERROR> Plaintext type [<class 'dict'>] not supported for encryption"

        '''
        self.classes_mean: np.ndarray of shape (12011,) (which is equal to the number of self.num_features)
        self.classes_variance: np.ndarray of shape (12011,) (which is equal to the number of self.num_features)
        self.prior: float 
        '''
        
        # we don't need to use these as pyfhel allows for ctxt + ptxt operations
        self.classes_mean_ctxt = np.empty((self.num_classes, self.num_features), dtype=PyCtxt)
        self.classes_variance_ctxt = np.empty((self.num_classes, self.num_features), dtype=PyCtxt)
        self.classes_prior_log_ctxt = np.empty((self.num_classes,), dtype=PyCtxt)
        # encrypt the density function constant
        self.density_func_constant_ctxt = np.empty((self.num_classes,), dtype=PyCtxt)


        for c in range(self.num_classes):
            self.classes_mean_ctxt[c] = HE.encrypt(self.classes_mean[str(c)])
            self.classes_variance_ctxt[c] = HE.encrypt(self.classes_variance[str(c)])
            self.classes_prior_log_ctxt[c] = HE.encrypt(np.log(self.classes_prior[str(c)]))

            const = -self.num_features / 2 * np.log(2 * np.pi) - 0.5 * np.sum(np.log(self.classes_variance[str(c)] + self.eps))
            # print("Class:", c)
            # print("Density function constant: ", const)
            self.density_func_constant_ctxt[c] = HE.encrypt(const)

        # save the HE context
        self.HE = HE

if __name__ == "__main__":
    X = np.load("data/X.npy")
    y = np.load("data/y.npy")


    print(X.shape)
    print(y.shape)
    NB = NaiveBayes(X,y)
    NB.fit(X, y)
    y_pred = NB.predict(X)

    print(sum(y_pred == y)/X.shape[0])
    print(sum(y)/y.shape[0])

