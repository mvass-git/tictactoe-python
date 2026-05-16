import socket
import threading

from commands import commands

import json

HOST, PORT = "0.0.0.0", 320

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(100)

def client_handler(client_socket, address):
    while True:
        try:
            pack = client_socket.recv(1024)

            if not pack:
                break
            msg = json.loads(pack.decode())
            type = msg.get("type")
            if type:
                commands[type]()
        except:
            pass
            

while True:
    client_socket, address = sock.accept()

    threading.Thread(target=client_handler, daemon=True).start()
