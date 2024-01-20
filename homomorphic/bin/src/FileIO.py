import pickle

def loadPickle(inputFilePath):
    data = None

    with open(inputFilePath, 'rb') as f:
        data = pickle.load(f)
    
    return data

def savePickle(outputFilePath, data):    
    with open(outputFilePath, 'wb') as f:
        pickle.dump(data, f)
