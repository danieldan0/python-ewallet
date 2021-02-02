import socket
import json

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = ''
        self.auth = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
    
    def login(self):
        self.id = input('Enter your ID: ')
        self.socket.sendall(bytes(json.dumps({
            'ACTION': 'LOGIN',
            'ID': self.id
        }) + '\n', 'utf-8'))
        self.auth = json.loads(str(self.socket.recv(1024), 'utf-8'))['AUTH']
    
    def loop(self, first):
        if self.auth:
            if first:
                print('Welcome to ewallet client! Enter "help" to see command list')
            command = input("> ")
            if command != "exit":
                self.loop(False)
