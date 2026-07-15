from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import Optional


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str
    scheduled_time: Optional[time] = None
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def is_complete(self) -> bool:
        """Return whether this task is completed."""
        return self.completed


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return self.pets

    def all_tasks(self) -> list[Task]:
        """Return every task from all of this owner's pets."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


@dataclass
class Scheduler:
    owner: Owner

    def get_all_tasks(self) -> list[Task]:
        """Return every task managed by the scheduler's owner."""
        return self.owner.all_tasks()

    def get_pending_tasks(self) -> list[Task]:
        """Return all tasks that are not completed."""
        return [task for task in self.get_all_tasks() if not task.is_complete()]

    def get_completed_tasks(self) -> list[Task]:
        """Return all tasks that are completed."""
        return [task for task in self.get_all_tasks() if task.is_complete()]

    def organize_tasks_by_pet(self) -> dict[str, list[Task]]:
        """Group tasks by pet name."""
        return {pet.name: pet.get_tasks() for pet in self.owner.get_pets()}

    def organize_tasks_by_frequency(self) -> dict[str, list[Task]]:
        """Group tasks by frequency."""
        tasks_by_frequency: dict[str, list[Task]] = {}
        for task in self.get_all_tasks():
            tasks_by_frequency.setdefault(task.frequency, []).append(task)
        return tasks_by_frequency

    def sort_tasks_by_time(self) -> list[Task]:
        """Return all tasks sorted by scheduled time."""
        return sorted(
            self.get_all_tasks(),
            key=lambda task: task.scheduled_time or time.max,
        )

    def mark_task_complete(self, task: Task) -> None:
        """Mark a managed task as completed."""
        task.mark_complete()
