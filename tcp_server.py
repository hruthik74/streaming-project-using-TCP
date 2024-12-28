import socket
import os
from concurrent.futures import ThreadPoolExecutor

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
VIDEO_FOLDER = 'static/videos/'  # Ensure this path exists and contains video files
MAX_WORKERS = 10  # Adjust based on expected load

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    try:
        # Receive the filename
        filename = client_socket.recv(1024).decode('utf-8')
        file_path = os.path.join(VIDEO_FOLDER, filename)

        # Check if the file exists
        if not os.path.isfile(file_path):
            client_socket.sendall(f"ERROR: File {filename} not found".encode('utf-8'))
            return

        # Send the file size
        file_size = os.path.getsize(file_path)
        client_socket.sendall(str(file_size).encode('utf-8'))

        # Wait for acknowledgment
        ack = client_socket.recv(1024).decode('utf-8')
        if ack != "ACK":
            print(f"Acknowledgment not received from {client_address}")
            return

        # Send the file in chunks
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):  # Stream in chunks
                client_socket.sendall(chunk)

        print(f"File {filename} sent successfully to {client_address}")

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"TCP server running on {SERVER_HOST}:{SERVER_PORT}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            client_socket, client_address = server.accept()
            executor.submit(handle_client, client_socket, client_address)

if __name__ == "__main__":
    start_tcp_server()