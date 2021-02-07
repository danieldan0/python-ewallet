import socketserver
from threading import Thread
import json
from database import *

class ClientThread(Thread):
    def __init__(self, ip, port, clientsocket, conn):
        super().__init__()
        self.conndir = conn
        self.conn = None
        self.ip = ip 
        self.port = port
        self.csocket = clientsocket
    
    def run(self):
        while True:
            self.data = json.loads(self.csocket.recv(1024).strip())
            print(self.data)
            if self.data['ACTION'] == 'EXIT':
                break
            self.conn = create_users_db(self.conndir)
            if self.data['ACTION'] == 'LOGIN':
                self.data = self.login()
            elif self.data['ACTION'] == 'BALANCE':
                self.data = self.balance()
            elif self.data['ACTION'] == 'ADDMONEY':
                self.data = self.add_money()
            elif self.data['ACTION'] == 'TRANSFER':
                self.data = self.transfer()
            elif self.data['ACTION'] == 'SETLIMIT':
                self.data = self.set_limit()
            elif self.data['ACTION'] == 'TEST':
                self.data = self.test()
            self.conn.close()
            self.csocket.send(self.data)
    
    def login(self):
        add_user(self.conn, self.data['ID'])
        return bytes(json.dumps({'AUTH': True}), 'utf-8')
    
    def balance(self):
        balance = get_balance(self.conn, self.data['ID'])
        return bytes(json.dumps({'AMOUNT': balance}), 'utf-8')
    
    def add_money(self):
        balance = get_balance(self.conn, self.data['ID'])
        balance_limit = get_balance_limit(self.conn, self.data['ID'])
        if balance_limit is None or balance_limit < 0 or (balance + self.data['AMOUNT']) <= balance_limit:
            if type(self.data['AMOUNT']) is int:
                set_balance(self.conn, self.data['ID'], balance + self.data['AMOUNT'])
                return bytes(json.dumps({'SUCCESS': True, 'AMOUNT': balance + self.data['AMOUNT'], 'ERROR': ''}), 'utf-8')
            else:
                return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Amount is not a number'}), 'utf-8')
        else:
            return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Limited by balance limit'}), 'utf-8')
    
    def transfer(self):
        balance = get_balance(self.conn, self.data['ID'])
        if get_user(self.conn, self.data['OTHERID']):
            otherbalance = get_balance(self.conn, self.data['OTHERID'])
            balance_limit = get_balance_limit(self.conn, self.data['OTHERID'])
            if balance_limit is None or balance_limit < 0 or (otherbalance + self.data['AMOUNT']) <= balance_limit:
                if (balance - self.data['AMOUNT']) >= 0:
                    if type(self.data['AMOUNT']) is int:
                        set_balance(self.conn, self.data['ID'], balance - self.data['AMOUNT'])
                        set_balance(self.conn, self.data['OTHERID'], otherbalance + self.data['AMOUNT'])
                        return bytes(json.dumps({'SUCCESS': True, 'AMOUNT': self.data['AMOUNT'], 'OTHERID': self.data['OTHERID'], 'ERROR': ''}), 'utf-8')
                    else:
                        return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Amount is not a number'}), 'utf-8')
                else:
                    return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Not enough money in account'}), 'utf-8')
            else:
                return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: Limited by balance limit'}), 'utf-8')
        else:
            return bytes(json.dumps({'SUCCESS': False, 'AMOUNT': balance, 'ERROR': 'Error: User does not exist'}), 'utf-8')
    
    def set_limit(self):
        set_balance_limit(self.conn, self.data['ID'], self.data['AMOUNT'])
        return bytes(json.dumps({'AMOUNT': self.data['AMOUNT']}), 'utf-8')

    def test(self):
        print(self.data['TEST'])
        return bytes(json.dumps({'TEST': self.data['TEST']}), 'utf-8')