import socket
import threading
import hashlib
import time
from datetime import datetime



# Configuration
host = "0.0.0.0"  # Listen on all available network interfaces
port = 50055  # Use the same port as in the sender script

hash_algorithm = "sha1"


def handle_client(conn, addr, req):
    received_file_path = f"received_{req}.npz"
    hasher = hashlib.new(hash_algorithm)
    now = datetime.now()
    tm = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{tm} - Connected by {addr}")
    # received_data = b""
    file_size = 0

    with open(received_file_path, "wb") as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
            hasher.update(data)
            file_size += len(data)
    now = datetime.now()
    tm = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{tm} - Hash of received file: {hasher.hexdigest()}")
    with open("receiver_report","at") as report:
        report.writelines(f"{hasher.hexdigest()},{file_size}\n")
    conn.close()


def main():
    with open("receiver_report","wt") as report:
        report.writelines("")
    req = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        now = datetime.now()
        tm = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{tm} - Server is listening for incoming connections...")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, req))
            thread.start()
            req += 1


if __name__ == "__main__":
    main()
