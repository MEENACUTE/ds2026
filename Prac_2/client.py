import xmlrpc.client
import sys

if len(sys.argv) != 2:
    print("Usage: python client.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
proxy = xmlrpc.client.ServerProxy('http://localhost:8000')

data = proxy.get_file(filename)
if data.data.startswith(b'File not found') or data.data.startswith(b'Error'):
    print(data.data.decode())
else:
    received_filename = f"received_{filename}"
    with open(received_filename, 'wb') as f:
        f.write(data.data)
    print(f"File received and saved as {received_filename}")