import socket
import json
import os

configpath = os.path.join(os.path.dirname(__file__), 'config.json')
config = json.load(open(configpath))

HOST = config['HOST']
PORT = config['SOCKETPORT']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)