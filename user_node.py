import socket
import sys

# Configuration for user node
CENTRAL_HOST = '127.0.0.1'
CENTRAL_PORT = 9000

def register_with_central(my_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CENTRAL_HOST, CENTRAL_PORT))
        s.sendall(f'register {my_port}'.encode())
        response = s.recv(1024)
        print("Central server response:", response.decode())

def deregister_with_central():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CENTRAL_HOST, CENTRAL_PORT))
        s.sendall('deregister'.encode())
        response = s.recv(1024)
        print("Central server response:", response.decode())

def query_peers():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CENTRAL_HOST, CENTRAL_PORT))
        s.sendall('query'.encode())
        response = s.recv(1024)
        print("Active peers:", response.decode())

def main(my_port):
    register_with_central(my_port)
    input("Press Enter to query peers...")
    query_peers()
    input("Press Enter to deregister...")
    deregister_with_central()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python user_node.py [PORT]")
        sys.exit(1)
    main(int(sys.argv[1]))
