from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

class FileTransferService:
    def get_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                return xmlrpc.client.Binary(f.read())
        except FileNotFoundError:
            return xmlrpc.client.Binary(b'File not found')
        except Exception as e:
            return xmlrpc.client.Binary(str(e).encode())

server = SimpleXMLRPCServer(('localhost', 8000))
server.register_instance(FileTransferService())
print("RPC server running on port 8000...")
server.serve_forever()