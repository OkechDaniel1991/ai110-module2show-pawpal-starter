from pawpal_system import Pet, Task


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
