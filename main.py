"""CLI testing ground for the PawPal+ logic layer.

Run with:  python main.py

Exercises the "smarter scheduling" features in the terminal before wiring
them into the Streamlit UI: sorting by time, filtering, recurring tasks,
and conflict detection.
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", available_minutes=90, preferences="mornings")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added deliberately out of time order, to prove sorting works.
    mochi.add_task(Task("Evening walk", "exercise", 30, 2, time="18:00"))
    mochi.add_task(Task("Morning walk", "exercise", 30, 3, time="08:00", frequency="daily"))
    mochi.add_task(Task("Midday play", "enrichment", 20, 1, time="12:00"))
    luna.add_task(Task("Feeding", "food", 10, 3, time="07:30"))
    # Same 08:00 slot as Mochi's morning walk -> a conflict.
    luna.add_task(Task("Vet meds", "health", 5, 3, time="08:00"))

    scheduler = Scheduler(owner)

    print("=== All tasks, sorted by time ===")
    for t in scheduler.sort_by_time():
        print(f"  {t.time}  {t.name} ({t.duration} min)")

    print("\n=== Filter: only Mochi's tasks ===")
    for t in scheduler.filter_tasks(pet_name="Mochi"):
        print(f"  {t.name} @ {t.time}")

    print("\n=== Conflict detection ===")
    conflicts = scheduler.detect_conflicts()
    print("\n".join(f"  {w}" for w in conflicts) if conflicts else "  No conflicts.")

    print("\n=== Recurring task ===")
    morning = mochi.tasks[1]  # the daily "Morning walk"
    upcoming = scheduler.mark_task_complete(morning)
    print(f"  Completed '{morning.name}' (daily). Next occurrence due: {upcoming.due_date}")

    print("\n=== Filter: pending (not completed) tasks ===")
    for t in scheduler.filter_tasks(completed=False):
        print(f"  {t.name} @ {t.time} (due {t.due_date})")


if __name__ == "__main__":
    main()
