import socketserver
import json
from database import *

class ServerTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.conn = server.conn
        super().__init__(request, client_address, server)
    
    def handle(self):
        self.data = json.loads(self.request.recv(1024).strip())
        print(self.data)
        if self.data['ACTION'] == 'LOGIN':
            self.login()
        elif self.data['ACTION'] == 'BALANCE':
            self.balance()
        elif self.data['ACTION'] == 'ADDMONEY':
            self.add_money()
        elif self.data['ACTION'] == 'TRANSFER':
            self.transfer()
        elif self.data['ACTION'] == 'SETLIMIT':
            self.set_limit()
        elif self.data['ACTION'] == 'TEST':
            self.test()
    
    def login(self):
        add_user(self.conn, self.data['ID'])
        self.request.sendall(bytes(json.dumps({'AUTH': True}), 'utf-8'))
    
    def balance(self):
        balance = get_balance(self.conn, self.data['ID'])
        self.request.sendall(bytes(json.dumps({'AMOUNT': balance}), 'utf-8'))
    
    def add_money(self):
        balance = get_balance(self.conn, self.data['ID'])
        balance_limit = get_balance_limit(self.conn, self.data['ID'])
        if (balance + self.data['AMOUNT']) <= balance_limit:
            if type(self.data['AMOUNT']) is int:
                set_balance(self.conn, self.data['ID'], balance + self.data['AMOUNT'])
                self.request.sendall(bytes(json.dumps({'SUCCESS': True, 'AMOUNT': balance + self.data['AMOUNT'], 'ERROR': ''}), 'utf-8'))
            else:
                self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Amount is not a number'}), 'utf-8'))
        else:
            self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Limited by balance limit'}), 'utf-8'))
    
    def transfer(self):
        balance = get_balance(self.conn, self.data['ID'])
        if get_user(self.conn, self.data['OTHERID']):
            otherbalance = get_balance(self.conn, self.data['OTHERID'])
            balance_limit = get_balance_limit(self.conn, self.data['OTHERID'])
            if (otherbalance + self.data['AMOUNT']) <= balance_limit:
                if (otherbalance - self.data['AMOUNT']) >= 0:
                    if type(self.data['AMOUNT']) is int:
                        set_balance(self.conn, self.data['ID'], balance - self.data['AMOUNT'])
                        set_balance(self.conn, self.data['OTHERID'], otherbalance + self.data['AMOUNT'])
                        self.request.sendall(bytes(json.dumps({'SUCCESS': True, 'AMOUNT': self.data['AMOUNT'], 'OTHERID': self.data['OTHERID'], 'ERROR': ''}), 'utf-8'))
                    else:
                        self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Amount is not a number'}), 'utf-8'))
                else:
                    self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Not enough money in account'}), 'utf-8'))
            else:
                self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Limited by balance limit'}), 'utf-8'))
        else:
            self.request.sendall(bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: User does not exist'}), 'utf-8'))
    
    def set_limit(self):
        set_balance_limit(self.conn, self.data['ID'], self.data['AMOUNT'])
        self.request.sendall(bytes(json.dumps({'AMOUNT': self.data['AMOUNT']}), 'utf-8'))

    def test(self):
        print(self.data['TEST'])
        self.request.sendall(bytes(json.dumps({'TEST': self.data['TEST']}), 'utf-8'))