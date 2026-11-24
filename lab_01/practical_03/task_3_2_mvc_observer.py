from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable


class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        pass


class SortByPriority(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.priority)


class SortByDeadline(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.deadline)


class SortByCreationDate(SortStrategy):
    def sort(self, tasks: list["Task"]) -> list["Task"]:
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


@dataclass
class Task:
    title: str
    priority: int
    deadline: datetime
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel(EventEmitter):
    def __init__(self):
        super().__init__()
        self._tasks: list[Task] = []

    def add_task(self, title: str, priority: int, deadline: datetime):
        task = Task(title=title, priority=priority, deadline=deadline)
        self._tasks.append(task)
        self.emit("task_added", task)

    def complete_task(self, index: int):
        if 0 <= index < len(self._tasks):
            self._tasks[index].completed = True
            self.emit("task_completed", self._tasks[index])

    def remove_task(self, index: int):
        if 0 <= index < len(self._tasks):
            task = self._tasks.pop(index)
            self.emit("task_removed", task)

    def get_tasks(self, include_completed: bool = True) -> list[Task]:
        if include_completed:
            return self._tasks[:]
        return [t for t in self._tasks if not t.completed]

    def get_statistics(self) -> dict:
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return {"total": total, "completed": completed, "active": total - completed}


class TaskView:
    def show_tasks(self, tasks: list[Task], title: str = "Завдання"):
        print(f"\n--- {title} ---")
        print(f"{'№':<3} | {'Назва':<20} | {'Пріор.':<7} | {'Дедлайн':<12} | {'Статус'}")
        print("-" * 65)
        for i, task in enumerate(tasks):
            status = "✅" if task.completed else "⏳"
            deadline_str = task.deadline.strftime("%d.%m")
            print(f"{i:<3} | {task.title:<20} | {task.priority:<7} | {deadline_str:<12} | {status}")
        print("-" * 65)

    def show_message(self, message: str):
        print(f"[INFO] {message}")

    def show_statistics(self, stats: dict):
        print(f"\n[СТАТИСТИКА] Всього: {stats['total']}, Активних: {stats['active']}, Виконано: {stats['completed']}")


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self._model = model
        self._view = view
        self._sort_strategy: SortStrategy = SortByPriority()

        self._model.on("task_added", lambda t: self._view.show_message(f"Додано завдання: '{t.title}'"))
        self._model.on("task_completed", lambda t: self._view.show_message(f"Виконано завдання: '{t.title}'"))
        self._model.on("task_removed", lambda t: self._view.show_message(f"Видалено завдання: '{t.title}'"))

    def set_sort_strategy(self, strategy: SortStrategy):
        self._sort_strategy = strategy

    def add_task(self, title: str, priority: int, deadline: datetime):
        self._model.add_task(title, priority, deadline)

    def complete_task(self, index: int):
        self._model.complete_task(index)

    def show_all(self):
        tasks = self._model.get_tasks()
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks)

    def show_active(self):
        tasks = self._model.get_tasks(include_completed=False)
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks, title="Активні завдання")

    def show_stats(self):
        self._view.show_statistics(self._model.get_statistics())


def main():
    model = TaskModel()
    view = TaskView()
    ctrl = TaskController(model, view)

    now = datetime.now()
    ctrl.add_task("Здати лабораторну", 1, now + timedelta(days=1))
    ctrl.add_task("Купить продукти", 3, now + timedelta(days=2))
    ctrl.add_task("Прочитати книгу", 4, now + timedelta(days=5))
    ctrl.add_task("Зателефонувати мамі", 2, now + timedelta(hours=5))

    print("\n--- Сортування за пріоритетом (за замовчуванням) ---")
    ctrl.show_all()

    print("\n--- Зміна стратегії на SortByDeadline ---")
    ctrl.set_sort_strategy(SortByDeadline())
    ctrl.show_all()

    print("\n--- Виконання завдання №1 ---")
    ctrl.complete_task(1)

    print("\n--- Тільки активні завдання ---")
    ctrl.show_active()

    ctrl.show_stats()


if __name__ == "__main__":
    main()
