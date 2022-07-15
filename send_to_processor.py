import socket

HOST = "127.0.0.1"
PORT = 65432

def process(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        data = s.recv(1024)

        print(f"Received data")

        return data
