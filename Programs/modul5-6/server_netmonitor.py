import socket
import threading

# Konfigurasi server
HOST = "127.0.0.1"
PORT = 12345
ADDR = (HOST, PORT)


def handle_device(client_socket):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            print(f"Data dari {addr}: {data.decode()}")
        except Exception as e:
            print(f"Error: {e}")
            break


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(ADDR)
        print(f"Server pemantauan berjalan di {HOST}:{PORT}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Menerima data dari {addr}")
            threading.Thread(
                target=handle_device, args=(server_socket,), daemon=True
            ).start()


if __name__ == "__main__":
    start_server()
