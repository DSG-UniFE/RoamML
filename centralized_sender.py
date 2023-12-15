import socket
import sys
import hashlib
import time
# python centralized_sender.py localhost 0

# Configuration
host = sys.argv[1]
port = 50055
node_id = sys.argv[2]

# Load the dataset from disk
file_path = f"./datasets/mnist-roamml/MNIST_subset_{node_id}.npz"

data_size = 0

time.sleep(5)

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    hasher = hashlib.new("sha1")
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(1024)
            if not chunk:
                break
            s.sendall(chunk)
            hasher.update(chunk)
            data_size += len(chunk)

    file_hash = hasher.hexdigest()
    print(f"File Hash: {file_hash}")

print(f"Node {node_id}: sent {data_size} bytes of data.")
