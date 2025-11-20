import socket
import os

HOST = '127.0.0.1'  # localhost
PORT = 65432        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # Receive filename from client
        filename = conn.recv(1024).decode('utf-8')
        print(f"Requested file: {filename}")
        
        if not os.path.exists(filename):
            conn.sendall(b'File not found')
        else:
            # Send file size
            filesize = os.path.getsize(filename)
            conn.sendall(str(filesize).encode('utf-8'))
            
            # Send file content in chunks
            with open(filename, 'rb') as f:
                while True:
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
            print("File sent successfully")