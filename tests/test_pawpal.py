"""Quick tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task's status to completed."""
    task = Task("Morning walk", "exercise", duration=30, priority=3)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "food", duration=10, priority=3))

    assert len(pet.tasks) == 1
