import json
import os
import sqlite3
from tcphandler import ServerTCPHandler
from server import SqliteTCPServer
from database import *


dirname = os.path.dirname(__file__)
configpath = os.path.join(dirname, 'config.json')
config = json.load(open(configpath))

conn = create_users_db(os.path.join(dirname, 'db.sqlite3'))

HOST = config['HOST']
PORT = config['SOCKETPORT']

if __name__ == '__main__':
    with SqliteTCPServer((HOST, PORT), ServerTCPHandler, conn) as server:
        server.serve_forever()