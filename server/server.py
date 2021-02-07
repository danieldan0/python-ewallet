import socketserver
class SqliteTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, conn, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.conn = conn