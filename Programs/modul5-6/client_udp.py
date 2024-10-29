import socket
import threading
import time
import random

# Konfigurasi klien
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
ADDR = (SERVER_HOST, SERVER_PORT)


def receive_updates(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print(f"\nUpdate dari server: {message.decode()}")
        except:
            break


def send_position(client_socket):
    while True:
        # Simulasikan posisi acak
        position = f"{random.randint(0, 100)},{random.randint(0, 100)}"
        client_socket.sendto(position.encode(), ADDR)
        time.sleep(1)  # Kirim update setiap detik


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Thread untuk menerima update
        thread = threading.Thread(target=receive_updates, args=(client_socket,))
        thread.start()

        # Thread untuk mengirim posisi
        send_position(client_socket)


if __name__ == "__main__":
    start_client()
