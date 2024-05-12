import socket
import sys
import threading

# Configuration for the central node

peers = {}  # Example: { '192.168.1.1': {'port': 1234, 'files': ['file1.txt', 'file2.txt']} }


def handle_client(conn, addr):
    with (conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode()
            if data.startswith('register'):
                _, port, *files = data.split()
                peers[addr[0]] = {'port': int(port), 'files': files}
                conn.sendall(b'Registered')
                print(f"Registered {addr[0]}:{port} with files {files}")
            elif data.startswith('deregister'):
                if addr[0] in peers:
                    del peers[addr[0]]
                    conn.sendall(b'Deregistered')
                print(f"Deregistered {addr[0]}")
            elif data.startswith('query'):
                response = "Peers:\n" + '       \n'.join(
                    f"{peer}:{details['port']}:{','.join(details['files'])}" for peer, details in peers.items())
                conn.sendall(response.encode())
                print(f"Queried by {addr[0]}")
            elif data.startswith('search'):
                _, filename = data.split()
                matching_peers = {}
                for peer, details in peers.items():
                    matched_files = [file for file in details['files'] if filename in file]
                    if matched_files:
                        matching_peers[peer] = {'port': details['port'], 'files': matched_files}
                response = "Search results:\n" + '      \n'.join(f"{peer}:{details['port']}:{','.join(details['files'])}" for peer, details in matching_peers.items())
                conn.sendall(response.encode() if response else b'No match found')
                print(f"Search for {filename} by {addr[0]}")


def main(central_host, central_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((central_host, central_port))
        s.listen()
        print(f"Central server listening on {central_host}:{central_port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python user_node.py [CENTRAL_HOST] [CENTRAL_PORT]")
        sys.exit(1)
    central_host = sys.argv[1]
    central_port = int(sys.argv[2])
    main(central_host, central_port)
