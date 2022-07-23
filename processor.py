import sys
import os
import socket
import src.FileIO as FileIO
import pickle
from socket_utils import send_msg, recv_msg
from dotenv import load_dotenv

# # definitions for sockets API
# HOST = "127.0.0.1"
# PORT = 65432

load_dotenv()

HOST = os.getenv('PROCESSOR_ADDR')
PORT = os.getenv('PROCESSOR_PORT')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, int(PORT)))
    while True:
        s.listen()
        print("Listenning for connection...")
        conn, addr = s.accept()

        with conn:
            print(f"Connection from: {addr}")

            received = recv_msg(conn)
            operation = pickle.loads(received)
            print("Received data")
            print("Running operation...")
            result = operation.run()
            print("Operation successfull. Sending back the results.")
            send_msg(conn, pickle.dumps(result))


########## replaced with sockets #############
# if len(sys.argv) <= 2:
#     print(f'Usage: {sys.argv[0]} inputFilePath outputFilePath')
#     sys.exit(1)

# inputFilePath = sys.argv[1]
# outputFilePath = sys.argv[2]

# operation = FileIO.loadPickle(inputFilePath)
#FileIO.savePickle(outputFilePath, result)
##############################################
