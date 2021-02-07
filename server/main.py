import json
import os
import sqlite3
from tcphandler import ClientThread
from database import *
import socket


dirname = os.path.dirname(__file__)
configpath = os.path.join(dirname, 'config.json')
config = json.load(open(configpath))

HOST = config['HOST']
PORT = config['SOCKETPORT']

if __name__ == '__main__':
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    tcpServer.bind((HOST, PORT)) 
    threads = [] 
    
    while True: 
        tcpServer.listen(4) 
        (clientsocket, (ip,port)) = tcpServer.accept() 
        newthread = ClientThread(ip, port, clientsocket, os.path.join(dirname, 'db.sqlite3')) 
        newthread.start() 
        threads.append(newthread) 