import socketserver
import json
import os
import sqlite3
from tcphandler import ServerTCPHandler
from database import *


dirname = os.path.dirname(__file__)
configpath = os.path.join(dirname, 'config.json')
config = json.load(open(configpath))

conn = create_users_db(os.path.join(dirname, 'db.sqlite3'))

HOST = config['HOST']
PORT = config['SOCKETPORT']

if __name__ == '__main__':
    with socketserver.TCPServer((HOST, PORT), ServerTCPHandler) as server:
        server.RequestHandlerClass.test = "test1234"
        server.serve_forever()