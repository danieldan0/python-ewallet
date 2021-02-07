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
        self.socket.send(bytes(json.dumps({
            'ACTION': 'LOGIN',
            'ID': self.id
        }) + '\n', 'utf-8'))
        self.auth = json.loads(str(self.socket.recv(1024), 'utf-8'))['AUTH']
    
    def loop(self, first):
        if self.auth:
            if first:
                print('Welcome to ewallet client! Enter "help" to see command list')
            command = input("> ")
            if command.startswith('help'):
                print('''Commands list:
help:
    shows command list
balance:
    shows balance
addmoney <amount>:
    adds money to your account
transfer <user> <amount>:
    transfers money to another account
setlimit <amount>:
    sets money limit on your account
exit:
    exit out of the client''')
            if command.startswith('balance'):
                self.socket.send(bytes(json.dumps({
                    'ACTION': 'BALANCE',
                    'ID': self.id
                }) + '\n', 'utf-8'))
                print(str(self.socket.recv(1024), 'utf-8'))
                print(json.loads(str(self.socket.recv(1024), 'utf-8'))['AMOUNT'] + "$")
            if command.startswith('addmoney'):
                if len(command.split()) > 1:
                    amount = command.split()[1]
                    self.socket.send(bytes(json.dumps({
                        'ACTION': 'ADDMONEY',
                        'AMOUNT': int(amount),
                        'ID': self.id
                    }) + '\n', 'utf-8'))
                else:
                    print("Error: amount argument is required")
            if command.startswith('transfer'):
                if len(command.split()) > 2 and command.split()[2].isdigit():
                    otherid = command.split()[1]
                    amount = command.split()[2]
                    self.socket.send(bytes(json.dumps({
                        'ACTION': 'TRANSFER',
                        'OTHERID': otherid,
                        'AMOUNT': int(amount),
                        'ID': self.id
                    }) + '\n', 'utf-8'))
                elif not command.split()[2].isdigit():
                    print("Error: amount must be a number")
                elif len(command.split()) > 1:
                    print("Error: amount argument is required")
                else:
                    print("Error: user and amount arguments are required")
            if command.startswith('setlimit'):
                if len(command.split()) > 1:
                    amount = command.split()[1]
                    self.socket.send(bytes(json.dumps({
                        'ACTION': 'SETLIMIT',
                        'AMOUNT': int(amount),
                        'ID': self.id
                    }) + '\n', 'utf-8'))
                else:
                    print("Error: amount argument is required")
            if command.startswith('test'):
                if len(command.split()) > 1:
                    test = command.split()[1]
                    self.socket.send(bytes(json.dumps({
                        'ACTION': 'TEST',
                        'TEST': test,
                        'ID': self.id
                    }) + '\n', 'utf-8'))
                    print(json.loads(str(self.socket.recv(1024), 'utf-8'))['TEST'])
                else:
                    print("Error: test argument is required")
            if command != "exit":
                self.loop(False)
