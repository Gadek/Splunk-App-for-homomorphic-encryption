import numpy as np
from Pyfhel import Pyfhel
import sys

import src.FileIO as FileIO

if len(sys.argv) <= 2:
    print(f'Usage: {sys.argv[0]} inputFilePath outputFilePath')
    sys.exit(1)

inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]

operation = FileIO.loadPickle(inputFilePath)
result = operation.run()

FileIO.savePickle(outputFilePath, result)
