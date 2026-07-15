from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_time(task_time: time | None) -> str:
    if task_time is None:
        return "Unscheduled"
    return task_time.strftime("%I:%M %p").lstrip("0")


def find_pet_name(task: Task, tasks_by_pet: dict[str, list[Task]]) -> str:
    for pet_name, pet_tasks in tasks_by_pet.items():
        if task in pet_tasks:
            return pet_name
    return "Unknown pet"


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever")
    luna = Pet(name="Luna", species="Cat", breed="Tabby")

    mochi.add_task(
        Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            scheduled_time=time(8, 0),
        )
    )
    luna.add_task(
        Task(
            description="Breakfast feeding",
            duration_minutes=10,
            frequency="daily",
            scheduled_time=time(9, 0),
        )
    )
    mochi.add_task(
        Task(
            description="Evening medication",
            duration_minutes=5,
            frequency="daily",
            scheduled_time=time(18, 30),
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    tasks_by_pet = scheduler.organize_tasks_by_pet()

    print("Today's Schedule")
    print("================")

    for task in scheduler.sort_tasks_by_time():
        pet_name = find_pet_name(task, tasks_by_pet)
        task_time = format_time(task.scheduled_time)
        print(
            f"{task_time} - {pet_name}: {task.description} "
            f"({task.duration_minutes} min, {task.frequency})"
        )


if __name__ == "__main__":
    main()
