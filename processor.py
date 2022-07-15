import numpy as np
from Pyfhel import Pyfhel
import sys
import socket
import src.FileIO as FileIO
import pickle

# definitions for sockets API
HOST = "127.0.0.1"
PORT = 65432


########## replace with sockets #############
# if len(sys.argv) <= 2:
#     print(f'Usage: {sys.argv[0]} inputFilePath outputFilePath')
#     sys.exit(1)

# inputFilePath = sys.argv[1]
# outputFilePath = sys.argv[2]

# operation = FileIO.loadPickle(inputFilePath)
##############################################

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("Listenning for connection...")
    conn, addr = s.accept()

    with conn:
        print(f"Connection from: {addr}")
        while True:
            operation = pickle.loads(conn.recv(1024))
            result = operation.run()

            #FileIO.savePickle(outputFilePath, result)
