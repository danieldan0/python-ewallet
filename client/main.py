import json
import os
from client import Client

dirname = os.path.dirname(__file__)
configpath = os.path.join(dirname, 'config.json')
config = json.load(open(configpath))

HOST = config['HOST']
PORT = config['SOCKETPORT']

wallet_client = Client(HOST, PORT)
wallet_client.login()
wallet_client.loop(True)