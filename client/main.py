import socket
from client import Client

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

wallet_client = Client(HOST, PORT)
wallet_client.login()
wallet_client.loop(True)