import commands
import json

def send_by_id(id, msg):
    for c in commands.clients:
        if c[1] == id:
            c[0].sendall(json.dumps(msg).encode())