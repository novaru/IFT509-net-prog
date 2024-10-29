import socket
import time

# Konfigurasi klien
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
ADDR = (SERVER_HOST, SERVER_PORT)


def send_data():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            message = "Status perangkat: OK"
            client_socket.sendto(message.encode(), ADDR)
            time.sleep(5)  # Kirim status setiap 5 detik


if __name__ == "__main__":
    send_data()
