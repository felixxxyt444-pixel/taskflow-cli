"""Ядро TaskFlow: задачи и менеджер задач."""
import json
from dataclasses import dataclass, asdict
from datetime import date
from typing import List, Optional

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    deadline: Optional[str] = None  # YYYY-MM-DD


class TaskManager:
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self._next_id = 1

    def add(self, title: str, priority: str = "medium", deadline: Optional[str] = None) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Название задачи не может быть пустым")
        if priority not in PRIORITIES:
            raise ValueError(f"Приоритет должен быть одним из {PRIORITIES}")
        if deadline:
            date.fromisoformat(deadline)  # ValueError при неверном формате
        task = Task(self._next_id, title, priority, False, deadline)
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"Задача {task_id} не найдена")

    def mark_done(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        return task

    def delete(self, task_id: int) -> None:
        self.tasks.remove(self.get(task_id))

    def list(self, status: Optional[str] = None) -> List[Task]:
        """status: None — все, 'done' — выполненные, 'todo' — невыполненные."""
        if status == "done":
            return [t for t in self.tasks if t.done]
        if status == "todo":
            return [t for t in self.tasks if not t.done]
        return list(self.tasks)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        try:
            with open(path, encoding="utf-8") as f:
                self.tasks = [Task(**item) for item in json.load(f)]
        except FileNotFoundError:
            self.tasks = []
        self._next_id = max((t.id for t in self.tasks), default=0) + 1
