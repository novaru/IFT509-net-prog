import threading
import time


def traffic_ligh(name, duration):
    colors = ["Merah", "Kuning", "Hijau"]
    while True:
        for color in colors:
            time.sleep(duration)
            print(f"{name} - {color}")


light1 = threading.Thread(target=traffic_ligh, args=("Lampu 1", 2))
light2 = threading.Thread(target=traffic_ligh, args=("Lampu 2", 2))

light1.start()
light2.start()

light1.join()
light2.join()
