import socket
import struct
from dotenv import load_dotenv
import os

PROCESSOR_ADDR = "127.0.0.1"
PROCESSOR_PORT = 65432

def process(msg):
    '''
    Send data to processor
    TODO: change the location of this function - it is related to hash_report operations not socket_utils
    '''
    load_dotenv()

    host = os.getenv('PROCESSOR_ADDR')
    port = os.getenv('PROCESSOR_PORT')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((PROCESSOR_ADDR, PROCESSOR_PORT))
        send_msg(s, msg)
        print("Data sent.")

        data = recv_msg(s)
        print(f"Received data")

    return data

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    print(f"length: {len(msg)}")
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    print(f"length: {msglen}")
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data