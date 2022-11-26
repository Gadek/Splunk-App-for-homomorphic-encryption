'''
[PROCESSOR SIDE]
the file vocabulary.txt is generated at the processor's side but it has to be distributed to the clients in order to encode the data before encryption
The purpose of this script is to build or update the existing vocabulary base in the vocabulary.txt file
'''

import pandas as pd
import numpy as np
import os
import nltk
from nltk.corpus import words
import pickle

DATA_DIR = "data"
EMAILS_FILE = "emails.csv"
VOCAB_FILE = "vocabulary.txt"

# set nltk module
nltk.download("words")
set_words = set(words.words())

data = pd.read_csv(DATA_DIR + "/" + EMAILS_FILE)
vocabulary = {}
# we want to have an easy way to go between the word in dict to its index which could than be easilly looked up by the algorithm
# (when using FHE we want to compare and group integers and NOT strings -> TODO: verify if we can improve that at a later stage)


def build_vocabulary(df_email: pd.DataFrame):
    '''The function updates the 'vocabulary' dictionary. 

    @param email_text: this is the text of one email message in the for of pandas DataFrame
    '''
    vocabulary_size = len(vocabulary)
    index = len(vocabulary)  # we retrieve the current NEXT value of the index where we can (potentially) add the new word
    for word in df_email:
        if word.lower() not in vocabulary and word.lower() in set_words:
            vocabulary[word.lower()] = index
            index += 1

def reduce_vocabulary_size(reduction_factor: float):
    assert reduction_factor < 1.0 and reduction_factor > 0
    vocab_reduced = dict(list(vocabulary.items())[:int(len(vocabulary) * reduction_factor)])
    return vocab_reduced

if __name__ == "__main__":
    for i in range(data.shape[0]):
        df_email = data.iloc[i, :][0].split()

        # print(
        #     f"Current email is {i}/{data.shape[0]} and the \
        #        length of vocab is curr {len(vocabulary)}"
        # )

        build_vocabulary(df_email)


    isExist = os.path.exists(DATA_DIR)
    if not isExist:
        os.makedirs(DATA_DIR)

    # we create a vocabulary with only 10% of the words available
    # vocabulary = reduce_vocabulary_size(0.1)
    print(f"Saving the vocabulary of length: {len(vocabulary)}")
    # dump to file
    pickle.dump( vocabulary, open(DATA_DIR + "/" + VOCAB_FILE, "wb") )

