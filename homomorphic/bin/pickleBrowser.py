#!bin/python -i

import src.FileIO as FileIO
import sys

if len(sys.argv) <= 1:
    print("Usage:", sys.argv[0], "[pickleFileToLoad]")
else:
    inputFile = sys.argv[1]
    data = FileIO.loadPickle(inputFile)

    print('Loaded pickle into variable data.')
    print('Execute "Pickle.save(data, \'outputPath\')" to save it.')
print("You are now in the Python interpreter.")
print("Press ctrl-d to exit.")
