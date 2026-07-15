from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str
    scheduled_time: Optional[time] = None
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def is_complete(self) -> bool:
        """Return whether this task is completed."""
        return self.completed

    def next_due_date(self, completed_on: Optional[date] = None) -> Optional[date]:
        """Calculate the next due date for supported recurring tasks.

        Daily tasks move forward by one day and weekly tasks move forward by
        seven days. Non-recurring or unsupported frequencies return None so the
        scheduler knows not to create a follow-up task.
        """
        recurrence_days = {
            "daily": 1,
            "weekly": 7,
        }
        days = recurrence_days.get(self.frequency.lower())

        if days is None:
            return None

        start_date = completed_on or date.today()
        return start_date + timedelta(days=days)


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

    def sort_by_time(self) -> list[Task]:
        """Return all tasks ordered from earliest scheduled time to latest.

        Tasks without a scheduled time are placed at the end. The sorting key
        uses each task's scheduled_time, which keeps the algorithm short and
        readable while preserving the original Task objects.
        """
        return self.sort_tasks_by_time()

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        """Return tasks matching the requested status and/or pet name.

        Passing completed=True returns completed tasks, completed=False returns
        pending tasks, and leaving it as None includes both. Passing pet_name
        narrows the results to one pet using a case-insensitive comparison.
        """
        tasks: list[Task] = []

        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue

            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                tasks.append(task)

        return tasks

    def find_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Return the pet that owns a task, if it is managed by this scheduler."""
        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                return pet
        return None

    def detect_conflicts(self, include_completed: bool = False) -> list[str]:
        """Return warning messages for tasks scheduled at the exact same time.

        This is a lightweight conflict check: it groups tasks by scheduled_time
        and reports any group with more than one task. By default, completed
        tasks are ignored so past tasks do not create noisy warnings.
        """
        tasks_by_time: dict[time, list[tuple[str, Task]]] = {}

        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                if task.scheduled_time is None:
                    continue
                if task.completed and not include_completed:
                    continue
                tasks_by_time.setdefault(task.scheduled_time, []).append((pet.name, task))

        warnings: list[str] = []
        for scheduled_time, task_entries in sorted(tasks_by_time.items()):
            if len(task_entries) < 2:
                continue

            time_label = scheduled_time.strftime("%I:%M %p").lstrip("0")
            task_labels = [
                f"{pet_name}: {task.description}"
                for pet_name, task in task_entries
            ]
            warnings.append(
                f"Warning: {len(task_entries)} tasks are scheduled at "
                f"{time_label}: {', '.join(task_labels)}."
            )

        return warnings

    def mark_task_complete(
        self,
        task: Task,
        completed_on: Optional[date] = None,
    ) -> Optional[Task]:
        """Mark a task complete and create its next recurring instance.

        Daily and weekly tasks are copied onto the same pet with a new due_date
        calculated by Task.next_due_date(). Non-recurring tasks simply become
        complete and return None.
        """
        task.mark_complete()

        next_due = task.next_due_date(completed_on)
        pet = self.find_pet_for_task(task)

        if next_due is None or pet is None:
            return None

        next_task = Task(
            description=task.description,
            duration_minutes=task.duration_minutes,
            frequency=task.frequency,
            scheduled_time=task.scheduled_time,
            completed=False,
            due_date=next_due,
        )
        pet.add_task(next_task)
        return next_task
