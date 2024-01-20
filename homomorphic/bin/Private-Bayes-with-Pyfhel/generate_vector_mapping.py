'''
[CLIENT SIDE]
For each email maps it into a vector of words, with subsequent quantities:
email:  [hello, ..., bitcoin, free, ..., Sincerely, ...]
vector: [   1,  ...,    3,      7,  ...,      1,    ...]
'''

import numpy as np
import pandas as pd
import pickle 
from collections.abc import Iterable    # ???

data = pd.read_csv('data/emails.csv')
vocabulary = pickle.load(open('data/vocabulary.txt', 'rb'))
X = np.zeros((data.shape[0], len(vocabulary)))      # shape = (size of the emails dataset, num of words in the vocabulary)
y = np.zeros((data.shape[0]))                       # shape = (size of the emails dataset,)


def generate_vector(email: Iterable) -> np.ndarray:
    if isinstance(email, str):
        raise Exception("The function will iterate over words in the email - make sure to split the string before passing it to the function")
    vect = np.zeros((len(vocabulary)))
    for word in email:
        if word.lower() in vocabulary:
            vect[vocabulary[word.lower()]] += 1         # X[index, the specific word index in the vocabulary dataset]
    
    return vect
    

if __name__ == "__main__":

    for i in range(data.shape[0]):
        email = data.iloc[i, :][0].split()

        for word in email:
            if word.lower() in vocabulary:
                X[i, vocabulary[word.lower()]] += 1         # X[index, the specific word index in the vocabulary dataset]
        
        y[i] = data.iloc[i, :][1]                   # spam or not spam classes in the 0-1 numerical format

    # Save stored numpy arrays
    np.save("data/X.npy", X)
    np.save("data/y.npy", y)