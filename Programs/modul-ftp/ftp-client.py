import socket
import os

# Client Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 2121
BUFFER_SIZE = 1024

def print_menu():
    """Display menu options to the user."""
    print("\n=== FTP Client Menu ===")
    print("1. List files on server")
    print("2. Upload file to server")
    print("3. Download file from server")
    print("4. Create directory on server")
    print("5. Remove directory on server")
    print("6. Quit")
    print("=======================\n")

def start_client():
    # Create and connect socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[CONNECTED] Connected to FTP server.")
    
    while True:
        print_menu()
        try:
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':  # List files
                client_socket.send("LIST".encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print("\nFiles on server:")
                print(response)
                
            elif choice == '2':  # Upload file
                filepath = input("Enter the path of the file to upload: ").strip()
                if os.path.exists(filepath):
                    filename = os.path.basename(filepath)
                    client_socket.send(f"UPLOAD {filename}".encode())
                    with open(filepath, 'rb') as f:
                        while (data := f.read(BUFFER_SIZE)):
                            client_socket.send(data)
                        client_socket.send(b'DONE')
                    response = client_socket.recv(BUFFER_SIZE).decode()
                    print(response)
                else:
                    print("File not found. Please check the path.")
                    
            elif choice == '3':  # Download file
                filename = input("Enter the name of the file to download: ").strip()
                client_socket.send(f"DOWNLOAD {filename}".encode())
                save_path = os.path.join(os.getcwd(), filename)
                with open(save_path, 'wb') as f:
                    while True:
                        data = client_socket.recv(BUFFER_SIZE)
                        if data == b'DONE':
                            break
                        f.write(data)
                print(f"File {filename} downloaded to {save_path}.")
                
            elif choice == '4':  # Create directory
                dirname = input("Enter the name of the directory to create: ").strip()
                client_socket.send(f"MKDIR {dirname}".encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print(response)
                
            elif choice == '5':  # Remove directory
                dirname = input("Enter the name of the directory to remove: ").strip()
                client_socket.send(f"RMDIR {dirname}".encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print(response)
                
            elif choice == '6':  # Quit
                client_socket.send("QUIT".encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print(response)
                break
                
            else:
                print("Invalid choice. Please select 1-6.")
                
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    
    client_socket.close()
    print("[DISCONNECTED] Client closed connection.")

if __name__ == "__main__":
    start_client()
