import socket
import threading

import json

HOST, PORT = "0.0.0.0", 320

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.listen(100)

def client_handler(client_socket, address):
    while True:
        try:
            pack = client_socket.recv(1024)

            if not pack:
                break
            msg = json.loads(pack.decode())
            

while True:
    client_socket, address = sock.accept()

    threading.Thread(target=client_handler, daemon=True).start()
