"""CLI testing ground for the PawPal+ logic layer.

Run with:  python main.py

This is a temporary script to verify the backend works in the terminal
before wiring it into the Streamlit UI.
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # An owner with a limited daily time budget.
    owner = Owner(name="Jordan", available_minutes=60, preferences="mornings")

    # Two pets.
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # A few tasks with different durations and priorities.
    mochi.add_task(Task("Morning walk", "exercise", duration=30, priority=3))
    mochi.add_task(Task("Feeding", "food", duration=10, priority=3))
    luna.add_task(Task("Litter box", "cleaning", duration=15, priority=2))
    luna.add_task(Task("Play/enrichment", "enrichment", duration=20, priority=1))
    # This one is already done, so the scheduler should skip it.
    mochi.add_task(Task("Give meds", "health", duration=5, priority=3, completed=True))

    scheduler = Scheduler(owner)

    print(scheduler.display_plan())
    print()
    print(scheduler.explain())


if __name__ == "__main__":
    main()
