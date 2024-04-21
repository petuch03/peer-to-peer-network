import socket
import threading

# Configuration for the central node
HOST = '127.0.0.1'
PORT = 9000

# Dictionary to keep track of active peers
peers = {}

def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode()
            if data.startswith('register'):
                _, port = data.split()
                peers[addr[0]] = int(port)
                conn.sendall(b'Registered')
            elif data.startswith('deregister'):
                if addr[0] in peers:
                    del peers[addr[0]]
                    conn.sendall(b'Deregistered')
            elif data.startswith('query'):
                response = ', '.join(f"{peer}:{port}" for peer, port in peers.items())
                conn.sendall(response.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Central server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
