import socket
import threading
import traceback

from commands import commands, clients, close_lobby, delete_client

import json

HOST, PORT = "0.0.0.0", 320

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(100)


def client_handler(client_socket, address):
    clients.append((client_socket, address))
    print(f"Client with address {address} connected.")
    try:
        buffer = ""
        while True:
            
                pack = client_socket.recv(1024)

                if not pack:
                    break
                buffer += pack.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line:
                        continue
                    msg = json.loads(line)
                    type = msg.get("type")
                    print(f"GOT MESSAGE from {address}: {msg}")
                    if type:
                        respond = commands[type](address, **msg)
                        if respond:
                            client_socket.sendall((json.dumps(respond) + "\n").encode())
    except:
        print(traceback.format_exc())
    finally:
         close_lobby(address, "Player left the lobby.")
         delete_client(address)
         client_socket.close()
            

while True:
    client_socket, address = sock.accept()

    threading.Thread(target=client_handler, args=(client_socket, address), daemon=True).start()
