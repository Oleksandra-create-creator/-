import threading
import queue
import time
import random


class Task:
    def __init__(self, task_id: int, data: str, priority: int = 0):
        self.task_id = task_id
        self.data = data
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        return f"Task(id={self.task_id}, data='{self.data}')"


def producer(task_queue: queue.Queue, num_tasks: int, producer_id: int) -> None:
    for i in range(num_tasks):
        task = Task(
            task_id=producer_id * 100 + i,
            data=f"Дані від виробника {producer_id}, пакет {i}",
            priority=random.randint(1, 5),
        )
        task_queue.put(task)
        print(f"  [Виробник-{producer_id}] Створено задачу {task.task_id}")
        time.sleep(random.uniform(0.05, 0.15))
    
    task_queue.put(None)


def consumer(task_queue: queue.Queue, consumer_id: int, results: list, results_lock: threading.Lock) -> None:
    while True:
        try:
            task = task_queue.get(timeout=2)
        except queue.Empty:
            print(f"  [Споживач-{consumer_id}] Черга порожня, завершення")
            break

        if task is None:
            task_queue.put(None)
            break

        work_time = random.uniform(0.1, 0.3)
        time.sleep(work_time)
        
        with results_lock:
            results.append({
                "task_id": task.task_id,
                "consumer": consumer_id,
                "time": work_time
            })
        
        task_queue.task_done()


def producer_consumer_demo():
    task_queue = queue.Queue(maxsize=5)
    results = []
    results_lock = threading.Lock()
    num_producers = 2
    num_consumers = 3
    tasks_per_producer = 5

    producers = []
    for i in range(num_producers):
        t = threading.Thread(target=producer, args=(task_queue, tasks_per_producer, i))
        producers.append(t)
        t.start()

    consumers = []
    for i in range(num_consumers):
        t = threading.Thread(target=consumer, args=(task_queue, i, results, results_lock))
        consumers.append(t)
        t.start()

    for t in producers:
        t.join()
    for t in consumers:
        t.join()

    print(f"\nОброблено задач: {len(results)}")
    if results:
        avg_time = sum(r["time"] for r in results) / len(results)
        print(f"Середній час обробки: {avg_time:.3f} сек")


def deadlock_demo():
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    deadlock_detected = threading.Event()

    def worker_1():
        lock_a.acquire()
        print("[Worker-1] Захопив Lock A")
        time.sleep(0.1)
        acquired = lock_b.acquire(timeout=2)
        if not acquired:
            print("[Worker-1] ДЕДЛОК: не вдалося захопити Lock B!")
            deadlock_detected.set()
            lock_a.release()
            return
        print("[Worker-1] Захопив Lock B")
        lock_b.release()
        lock_a.release()

    def worker_2():
        lock_b.acquire()
        print("[Worker-2] Захопив Lock B")
        time.sleep(0.1)
        acquired = lock_a.acquire(timeout=2)
        if not acquired:
            print("[Worker-2] ДЕДЛОК: не вдалося захопити Lock A!")
            deadlock_detected.set()
            lock_b.release()
            return
        print("[Worker-2] Захопив Lock A")
        lock_a.release()
        lock_b.release()

    def safe_worker_1():
        with lock_a:
            print("[Safe-Worker-1] Захопив Lock A")
            time.sleep(0.1)
            with lock_b:
                print("[Safe-Worker-1] Захопив Lock B")

    def safe_worker_2():
        with lock_a:
            print("[Safe-Worker-2] Захопив Lock A")
            time.sleep(0.1)
            with lock_b:
                print("[Safe-Worker-2] Захопив Lock B")

    print("=== Спроба з потенційним дедлоком ===")
    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    if deadlock_detected.is_set():
        print(">>> Дедлок виявлено! Використовуємо timeout для запобігання зависанню.\n")
    else:
        print(">>> Дедлок не виник цього разу (залежить від планувальника).\n")

    print("=== Безпечна версія (однаковий порядок замків) ===")
    s1 = threading.Thread(target=safe_worker_1)
    s2 = threading.Thread(target=safe_worker_2)
    s1.start()
    s2.start()
    s1.join()
    s2.join()
    print(">>> Безпечна версія виконалася без дедлоків.")


def main():
    print("=" * 60)
    print("=== Паттерн Producer-Consumer ===")
    print("=" * 60)
    producer_consumer_demo()

    print(f"\n{'=' * 60}")
    print("=== Демонстрація дедлоку ===")
    print("=" * 60)
    deadlock_demo()


if __name__ == "__main__":
    main()
