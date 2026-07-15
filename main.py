from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_time(task_time: time | None) -> str:
    if task_time is None:
        return "Unscheduled"
    return task_time.strftime("%I:%M %p").lstrip("0")


def format_due_date(due_date: date | None) -> str:
    if due_date is None:
        return "No due date"
    return due_date.strftime("%Y-%m-%d")


def find_pet_name(task: Task, tasks_by_pet: dict[str, list[Task]]) -> str:
    for pet_name, pet_tasks in tasks_by_pet.items():
        if task in pet_tasks:
            return pet_name
    return "Unknown pet"


def sort_task_list_by_time(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda task: task.scheduled_time or time.max)


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    luna = Pet(name="Luna", species="Cat", breed="Tabby")

    evening_medication = Task(
        description="Evening medication",
        duration_minutes=5,
        frequency="daily",
        scheduled_time=time(18, 30),
    )
    breakfast_feeding = Task(
        description="Breakfast feeding",
        duration_minutes=10,
        frequency="daily",
        scheduled_time=time(9, 0),
        due_date=date.today(),
    )
    morning_walk = Task(
        description="Morning walk",
        duration_minutes=30,
        frequency="daily",
        scheduled_time=time(8, 0),
    )
    litter_box_cleanup = Task(
        description="Litter box cleanup",
        duration_minutes=10,
        frequency="daily",
        scheduled_time=time(8, 0),
    )

    # Add tasks out of order so the sorting logic is easy to verify.
    mochi.add_task(evening_medication)
    luna.add_task(breakfast_feeding)
    mochi.add_task(morning_walk)
    luna.add_task(litter_box_cleanup)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(breakfast_feeding)
    tasks_by_pet = scheduler.organize_tasks_by_pet()

    def print_tasks(title: str, tasks: list[Task]) -> None:
        print(title)
        print("=" * len(title))
        for task in tasks:
            pet_name = find_pet_name(task, tasks_by_pet)
            task_time = format_time(task.scheduled_time)
            due_date = format_due_date(task.due_date)
            status = "complete" if task.completed else "pending"
            print(
                f"{task_time} - {pet_name}: {task.description} "
                f"({task.duration_minutes} min, {task.frequency}, "
                f"{status}, due {due_date})"
            )
        print()

    print_tasks("Today's Schedule", scheduler.sort_by_time())
    print_tasks(
        "Pending Tasks",
        sort_task_list_by_time(scheduler.filter_tasks(completed=False)),
    )
    print_tasks(
        "Completed Tasks",
        sort_task_list_by_time(scheduler.filter_tasks(completed=True)),
    )
    print_tasks(
        "Mochi's Tasks",
        sort_task_list_by_time(scheduler.filter_tasks(pet_name="Mochi")),
    )

    print("Schedule Warnings")
    print("=================")
    for warning in scheduler.detect_conflicts():
        print(warning)


if __name__ == "__main__":
    main()
