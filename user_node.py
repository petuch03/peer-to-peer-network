import socket
import sys
import threading
import multiprocessing
from colorama import Fore

LOCAL_HOST = '0.0.0.0'


def register_with_central(central_host, central_port, my_port, files):
    files_str = ' '.join(files)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((central_host, central_port))
        s.sendall(f'register {my_port} {files_str}'.encode())
        response = s.recv(1024)
        print("Central server response:", response.decode())


def deregister_with_central(central_host, central_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((central_host, central_port))
        s.sendall('deregister'.encode())
        response = s.recv(1024)
        print("Central server response:", response.decode())


def query_peers(central_host, central_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((central_host, central_port))
        s.sendall('query'.encode())
        response = s.recv(1024)
        print(response.decode())


def search_file(central_host, central_port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((central_host, central_port))
        s.sendall(f'search {filename}'.encode())
        response = s.recv(1024)
        print(response.decode())


def handle_peer_request(conn, addr):
    print(f"Connection from {addr} has been established.")
    with conn:
        request = conn.recv(1024).decode()
        if request.startswith('request'):
            _, filename = request.split()
            try:
                with open(filename, 'rb') as f:
                    while True:
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            break
                        conn.sendall(bytes_read)
                print(Fore.RED + f"Sent {filename} to {addr}"+ Fore.RESET)
            except FileNotFoundError:
                print(Fore.RED + f"File not found: {filename}" + Fore.RESET)
        else:
            print(Fore.RED + "Received unknown command" + Fore.RESET)


def start_file_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((LOCAL_HOST, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_peer_request, args=(conn, addr))
            thread.start()


def download_file_from_peer(ip, port, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(f'request {filename}'.encode())
        with open(filename, 'wb') as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        print(f"Downloaded {filename} from {ip}:{port}")


def main(central_host, central_port, my_port, files):
    file_server_process = multiprocessing.Process(target=start_file_server, args=(my_port,))
    file_server_process.start()

    while True:
        print("\nCommands:")
        print("1 - Register with central")
        print("2 - Deregister from central")
        print("3 - Query peers")
        print("4 - Download a file")
        print("5 - Search for a file")
        print("6 - Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_with_central(central_host, central_port, my_port, files)
        elif choice == '2':
            deregister_with_central(central_host, central_port)
        elif choice == '3':
            query_peers(central_host, central_port)
        elif choice == '4':
            peer = input("Enter peer IP, port and filename (ip:port:filename): ")
            ip, port, filename = peer.split(':')
            download_file_from_peer(ip, int(port), filename)
        elif choice == '5':
            filename = input("Enter filename to search: ")
            search_file(central_host, central_port, filename)
        elif choice == '6':
            deregister_with_central(central_host, central_port)
            print("Exiting program.")
            file_server_process.terminate()
            exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python user_node.py [CENTRAL_HOST] [CENTRAL_PORT] [MY_PORT] [FILE1] [FILE2] ...")
        sys.exit(1)
    central_host = sys.argv[1]
    central_port = int(sys.argv[2])
    my_port = int(sys.argv[3])
    my_files = sys.argv[4:]
    main(central_host, central_port, my_port, my_files)
