import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python client.py <filename> <output_filename>")
    sys.exit(1)

filename = sys.argv[1]
output_filename = sys.argv[2]

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Send filename to server
    s.sendall(filename.encode('utf-8'))
    
    # Receive file size/error
    response = s.recv(1024).decode('utf-8')
    if response == 'File not found':
        print("File not found on server")
    else:
        filesize = int(response)
        print(f"Receiving file of size {filesize} bytes")
        
        # Receive file content
        received = 0
        with open(output_filename, 'wb') as f:
            while received < filesize:
                bytes_read = s.recv(4096)
                if not bytes_read:
                    break
                f.write(bytes_read)
                received += len(bytes_read)
        print("File received successfully")