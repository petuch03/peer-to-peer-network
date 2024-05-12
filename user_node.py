import socket
import sys

# Configuration for user node
CENTRAL_HOST = '172.29.67.89'
CENTRAL_PORT = 9001

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
    while True:
        print("\nCommands:")
        print("1 - Register with central")
        print("2 - Deregister from central")
        print("3 - Query peers")
        print("4 - Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_with_central(my_port)
        elif choice == '2':
            deregister_with_central()
        elif choice == '3':
            query_peers()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python user_node.py [PORT]")
        sys.exit(1)
    my_port = int(sys.argv[1])
    main(my_port)
