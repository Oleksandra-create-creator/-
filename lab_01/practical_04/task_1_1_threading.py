import threading
import time


def download_simulation(file_name: str, size_mb: float) -> dict:
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Початок завантаження '{file_name}' ({size_mb} MB)...")
    time.sleep(size_mb * 0.2)
    return {"file": file_name, "size": size_mb, "thread": thread_name}


class MonitorThread(threading.Thread):
    def __init__(self, interval: float = 0.5):
        super().__init__(name="Monitor", daemon=True)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print(f"[Monitor] Активних потоків: {threading.active_count()}")
            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()


def main():
    files = [
        ("data.csv", 2.5),
        ("report.pdf", 1.0),
        ("image.png", 0.5),
        ("archive.zip", 4.0),
        ("log.txt", 0.3),
    ]

    monitor = MonitorThread()
    monitor.start()

    threads = []
    for file_name, size in files:
        t = threading.Thread(target=download_simulation, args=(file_name, size))
        threads.append(t)

    start = time.perf_counter()
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    elapsed = time.perf_counter() - start
    monitor.stop()
    
    print(f"\nУсі файли завантажено паралельно за {elapsed:.2f} сек")

    seq_start = time.perf_counter()
    for file_name, size in files:
        download_simulation(file_name, size)
    seq_elapsed = time.perf_counter() - seq_start
    
    print(f"Послідовне завантаження зайняло б: {seq_elapsed:.2f} сек")
    print(f"Прискорення: {seq_elapsed / elapsed:.2f}x")


if __name__ == "__main__":
    main()
