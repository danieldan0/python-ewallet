import socketserver
import json

class ServerTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = json.loads(self.rfile.readline().strip())
        if self.data['ACTION'] == 'LOGIN':
            self.login()
    
    def login(self):
        if hasattr(self, 'test'):
            print(self.test)
            print(self.client_address)
        self.wfile.write(bytes(json.dumps({'AUTH': True}), 'utf-8'))