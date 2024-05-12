import socket
import threading

# Configuration for the central node
HOST = '172.29.67.89'
PORT = 9001

peers = {}  # Example: { '192.168.1.1': {'port': 1234, 'files': ['file1.txt', 'file2.txt']} }

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode()
            if data.startswith('register'):
                _, port, *files = data.split()
                peers[addr[0]] = {'port': int(port), 'files': files}
                conn.sendall(b'Registered')
                print(f"Registered {addr} with files {files}")
            elif data.startswith('deregister'):
                if addr[0] in peers:
                    del peers[addr[0]]
                    conn.sendall(b'Deregistered')
                print(f"Deregistered {addr}")
            elif data.startswith('query'):
                response = str(len(peers)) + "::"
                response += ', '.join(f"{peer}:{details['port']}:{','.join(details['files'])}" for peer, details in peers.items())
                conn.sendall(response.encode())
                print(f"Queried by {addr}")

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
