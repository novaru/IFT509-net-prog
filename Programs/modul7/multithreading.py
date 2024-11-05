import threading
import time

# Fungsi yang akan dijalankan dalam thread
def print_numbers():
    for i in range(1,6):
        time.sleep(1)
        print(f"Number: {i}")

def print_letters():
    for letter in 'ABCDE':
        time.sleep(1.5)
        print(f"Letter: {letter}")

# Membuat thread
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Memulai thread
thread1.start()
thread2.start()

# Menunggu thread selesai
thread1.join()
thread2.join()

print("Program selesai.")
