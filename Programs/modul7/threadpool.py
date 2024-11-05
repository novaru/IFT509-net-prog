from concurrent.futures import ThreadPoolExecutor
import time


def task(n):
    print(f"Task {n} dimulai")
    time.sleep(2)
    print(f"Task {n} selesai")


# Membuat thread pool dengan 3 worker
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(task, i) for i in range(1, 6)]
    for future in futures:
        future.result()  # Menunggu hingga semua task selesai

print("Semua tugas selesai.")
