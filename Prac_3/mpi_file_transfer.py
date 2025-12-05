from mpi4py import MPI # type: ignore
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    if rank == 0:
        print("This program requires exactly 2 processes.")
    sys.exit(1)

CHUNK_SIZE = 1024 * 1024  #1MB chunk

if rank == 0:  #Server
    if len(sys.argv) != 2:
        print("Usage: mpirun -np 2 python mpi_file_transfer.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        # file_sz 1st
        file_size = len(file_data)
        comm.send(file_size, dest=1)
        
        # Data -> chunk
        for i in range(0, file_size, CHUNK_SIZE):
            chunk = file_data[i:i + CHUNK_SIZE]
            comm.send(chunk, dest=1)
        
        print(f"File '{filename}' sent successfully.")
    except FileNotFoundError:
        comm.send(-1, dest=1)  #Error
        print(f"File '{filename}' not found.")
    except Exception as e:
        comm.send(-1, dest=1)
        print(f"Error: {str(e)}")

elif rank == 1:  #Client
    file_size = comm.recv(source=0)
    if file_size == -1:
        print("Error receiving file.")
        sys.exit(1)
    
    received_data = b''
    remaining = file_size
    while remaining > 0:
        chunk_size = min(remaining, CHUNK_SIZE)
        chunk = comm.recv(source=0)
        received_data += chunk
        remaining -= len(chunk)
    
    received_filename = f"received_{sys.argv[1]}" if len(sys.argv) > 1 else "received_file"
    with open(received_filename, 'wb') as f:
        f.write(received_data)
    
    print(f"File received and saved as '{received_filename}' (size: {file_size} bytes).")