import socket
import threading
import traceback

from commands import commands, clients

import json

HOST, PORT = "0.0.0.0", 320

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(100)


def client_handler(client_socket, address):
    clients.append((client_socket, address))
    print(f"Client with address {address} connected.")
    try:
        while True:
            
                pack = client_socket.recv(1024)

                if not pack:
                    break
                msg = json.loads(pack.decode())
                type = msg.get("type")
                print(f"GOT MESSAGE from {address}: {msg}")
                if type:
                    respond = commands[type](address, **msg)
                    client_socket.sendall(json.dumps(respond).encode())
    except:
        print(traceback.format_exc())
    finally:
         client_socket.close()
            

while True:
    client_socket, address = sock.accept()

    threading.Thread(target=client_handler, args=(client_socket, address), daemon=True).start()
