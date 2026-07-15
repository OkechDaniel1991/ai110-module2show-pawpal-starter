from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_changes_status() -> None:
    task = Task(
        description="Morning walk",
        duration_minutes=30,
        frequency="daily",
    )

    task.mark_complete()

    assert task.is_complete()


def test_add_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    task = Task(
        description="Breakfast feeding",
        duration_minutes=10,
        frequency="daily",
    )

    starting_count = len(pet.get_tasks())
    pet.add_task(task)

    assert len(pet.get_tasks()) == starting_count + 1


def test_scheduler_sorts_tasks_by_time() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    late_task = Task("Dinner", 10, "daily", scheduled_time=time(18, 0))
    early_task = Task("Breakfast", 10, "daily", scheduled_time=time(8, 0))

    pet.add_task(late_task)
    pet.add_task(early_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == [early_task, late_task]


def test_scheduler_sorts_tasks_without_times_last() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    untimed_task = Task("Brush coat", 15, "weekly")
    morning_task = Task("Breakfast", 10, "daily", scheduled_time=time(8, 0))
    evening_task = Task("Dinner", 10, "daily", scheduled_time=time(18, 0))

    pet.add_task(untimed_task)
    pet.add_task(evening_task)
    pet.add_task(morning_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == [morning_task, evening_task, untimed_task]


def test_scheduler_handles_pet_with_no_tasks() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.get_all_tasks() == []
    assert scheduler.get_pending_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []


def test_scheduler_filters_tasks_by_status_and_pet_name() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    luna = Pet(name="Luna", species="Cat", breed="Tabby")
    completed_task = Task("Morning walk", 30, "daily", completed=True)
    pending_task = Task("Breakfast feeding", 10, "daily")

    mochi.add_task(completed_task)
    luna.add_task(pending_task)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=True) == [completed_task]
    assert scheduler.filter_tasks(pet_name="Luna") == [pending_task]
    assert scheduler.filter_tasks(completed=False, pet_name="Luna") == [pending_task]


def test_daily_task_completion_creates_next_daily_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="Cat", breed="Tabby")
    task = Task("Breakfast feeding", 10, "daily", scheduled_time=time(9, 0))
    completed_on = date(2026, 7, 15)

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task, completed_on=completed_on)

    assert task.is_complete()
    assert next_task is not None
    assert next_task.due_date == completed_on + timedelta(days=1)
    assert next_task in pet.get_tasks()
    assert not next_task.is_complete()


def test_weekly_task_completion_creates_next_weekly_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    task = Task("Grooming", 45, "weekly")
    completed_on = date(2026, 7, 15)

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task, completed_on=completed_on)

    assert next_task is not None
    assert next_task.due_date == completed_on + timedelta(days=7)


def test_non_recurring_task_completion_does_not_create_next_task() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="Cat", breed="Tabby")
    task = Task("One-time vet visit", 60, "once", scheduled_time=time(14, 0))

    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task, completed_on=date(2026, 7, 15))

    assert task.is_complete()
    assert next_task is None
    assert pet.get_tasks() == [task]


def test_scheduler_detects_tasks_at_same_time() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    luna = Pet(name="Luna", species="Cat", breed="Tabby")
    morning_walk = Task("Morning walk", 30, "daily", scheduled_time=time(8, 0))
    litter_cleanup = Task("Litter box cleanup", 10, "daily", scheduled_time=time(8, 0))

    mochi.add_task(morning_walk)
    luna.add_task(litter_cleanup)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == [
        "Warning: 2 tasks are scheduled at 8:00 AM: "
        "Mochi: Morning walk, Luna: Litter box cleanup."
    ]


def test_scheduler_returns_no_conflict_warnings_for_unique_times() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")

    pet.add_task(Task("Morning walk", 30, "daily", scheduled_time=time(8, 0)))
    pet.add_task(Task("Dinner", 10, "daily", scheduled_time=time(18, 0)))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == []


def test_scheduler_ignores_completed_tasks_when_detecting_conflicts() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    completed_task = Task(
        "Morning walk",
        30,
        "daily",
        scheduled_time=time(8, 0),
        completed=True,
    )
    pending_task = Task("Breakfast", 10, "daily", scheduled_time=time(8, 0))

    pet.add_task(completed_task)
    pet.add_task(pending_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    assert scheduler.detect_conflicts() == []
    assert scheduler.detect_conflicts(include_completed=True) == [
        "Warning: 2 tasks are scheduled at 8:00 AM: "
        "Mochi: Morning walk, Mochi: Breakfast."
    ]
