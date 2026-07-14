from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from enum import Enum
from typing import Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recurrence(Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class TimeWindow:
    start: time
    end: time

    def duration_minutes(self) -> int:
        pass

    def contains(self, t: time) -> bool:
        pass

    def overlaps(self, other: TimeWindow) -> bool:
        pass


@dataclass
class Owner:
    name: str
    availability: TimeWindow
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def all_tasks(self) -> list[Task]:
        pass

    def available_minutes(self) -> int:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    category: str
    recurrence: Recurrence
    weekdays: set[int] = field(default_factory=set)
    fixed_time: Optional[time] = None

    def is_fixed(self) -> bool:
        pass

    def occurs_on(self, day: date) -> bool:
        pass


@dataclass
class ScheduledTask:
    task: Task
    slot: TimeWindow

    def overlaps(self, other: ScheduledTask) -> bool:
        pass

    def label(self) -> str:
        pass


@dataclass
class Plan:
    day: date
    scheduled: list[ScheduledTask] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def add_scheduled(self, st: ScheduledTask) -> None:
        pass

    def add_skipped(self, task: Task, reason: str) -> None:
        pass

    def total_minutes(self) -> int:
        pass

    def is_empty(self) -> bool:
        pass

    def explain(self) -> str:
        pass


@dataclass
class Scheduler:
    day_bounds: TimeWindow

    def generate_plan(self, owner: Owner, day: date) -> Plan:
        pass

    def filter_due(self, tasks: list[Task], day: date) -> list[Task]:
        pass

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        pass

    def place_task(
        self, task: Task, taken: list[ScheduledTask]
    ) -> Optional[ScheduledTask]:
        pass

    def detect_conflict(self, a: ScheduledTask, b: ScheduledTask) -> bool:
        pass
