import socket
import sys
import hashlib
import time
# python centralized_sender.py localhost 0
from datetime import datetime



# Configuration
host = sys.argv[1]
port = 50055
node_id = sys.argv[2]

# Load the dataset from disk
file_path = f"./datasets/cifar10/CIFAR10_subset_{node_id}.npz"

data_size = 0

time.sleep(5)

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    hasher = hashlib.new("sha1")
    with open(file_path, "rb") as file:
        now = datetime.now()
        tm = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{tm} - beginning transmission")
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            s.sendall(chunk)
            hasher.update(chunk)
            data_size += len(chunk)

    file_hash = hasher.hexdigest()
    now = datetime.now()
    tm = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{tm} - File Hash: {file_hash}")

now = datetime.now()
tm = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"{tm} - Node {node_id}: sent {data_size} bytes of data.")
