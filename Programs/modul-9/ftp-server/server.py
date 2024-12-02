import socket
import os
import threading
import ssl

HOST = "127.0.0.1"
PORT = 2121
BASE_DIR = "files"  # Direktori penyimpanan file server
CERT_FILE = "server.crt"
KEY_FILE = "server.key"

USERS = {
    "admin": "password",
}

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)


def authenticate_client(client_socket):
    username = client_socket.recv(1024).decode().strip()
    password = client_socket.recv(1024).decode().strip()

    if username in USERS and USERS[username] == password:
        client_socket.send("[SUCCESS] Authentication successful.".encode())
        return True

    client_socket.send("[ERROR] Authentication failed.".encode())
    return False


def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    if not authenticate_client(client_socket):
        client_socket.close()
        return

    while True:
        try:
            command = client_socket.recv(1024).decode().strip()
            if not command:
                break

            if command == "LIST":
                file_list = []
                for root, _, files in os.walk(BASE_DIR):
                    rel_path = os.path.relpath(root, BASE_DIR)
                    if rel_path != ".":
                        file_list.append(f"\nDirectory: {rel_path}")
                    for file in files:
                        file_path = os.path.join(rel_path, file)
                        if rel_path == ".":
                            file_list.append(file)
                        else:
                            file_list.append(file_path)
                files = "\n".join(file_list)
                client_socket.send(files.encode())

            elif command.startswith("UPLOAD"):
                _, filename = command.split(maxsplit=1)
                filepath = os.path.join(BASE_DIR, filename)

                with open(filepath, "wb") as f:
                    while True:
                        data = client_socket.recv(1024)
                        if data.endswith(b"DONE"):
                            f.write(data[:-4])
                            break
                        f.write(data)

                client_socket.send(f"[SUCCESS] File {filename} uploaded.".encode())
            elif command.startswith("DOWNLOAD"):
                _, filename = command.split(maxsplit=1)
                filepath = os.path.join(BASE_DIR, filename)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        while data := f.read(1024):
                            client_socket.send(data)
                    client_socket.send(b"DONE")
                else:
                    client_socket.send("[ERROR] File not found.".encode())

            elif command.startswith("MKDIR"):
                _, dirname = command.split(maxsplit=1)
                dirpath = os.path.join(BASE_DIR, dirname)
                try:
                    os.makedirs(dirpath)
                    client_socket.send(
                        f"[SUCCESS] Directory {dirname} created.".encode()
                    )
                except Exception as e:
                    client_socket.send(
                        f"[ERROR] Could not create directory: {str(e)}".encode()
                    )

            elif command.startswith("RMDIR"):
                _, dirname = command.split(maxsplit=1)
                dirpath = os.path.join(BASE_DIR, dirname)
                try:
                    os.rmdir(dirpath)
                    client_socket.send(
                        f"[SUCCESS] Directory {dirname} removed.".encode()
                    )
                except Exception as e:
                    client_socket.send(
                        f"[ERROR] Could not remove directory: {str(e)}".encode()
                    )
            elif command == "QUIT":
                client_socket.send("[DISCONNECTED] Goodbye!".encode())
                break

            else:
                client_socket.send("[ERROR] Invalid command.".encode())
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break
    client_socket.close()
    print("[DISCONNECTED] Client closed connection.")


def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[STARTED] Server running on {HOST}:{PORT}")

    # Wrap the server socket with SSL using context
    server_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        try:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    start_server()
