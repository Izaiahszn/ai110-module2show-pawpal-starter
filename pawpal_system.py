"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant.

Design (from diagram.mmd, refined during implementation):
    Task      one care activity: name, category, duration, priority, completed
    Pet       a pet + the list of tasks it owns (add / edit / remove)
    Owner     an owner, their constraints, their pets; exposes all_tasks()
    Scheduler the "brain": reads the owner's tasks and builds/explains a plan

Priority convention: higher int = more important (3 = high, 2 = medium, 1 = low).
The daily plan lays tasks out sequentially starting from DAY_START.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# The plan lays tasks out back-to-back starting at this hour (24h clock).
DAY_START_HOUR = 8


@dataclass
class Task:
    """A single pet care activity.

    `name` acts as the task's identifier within a pet (used by edit/remove).
    `priority` is an int where higher = more important.
    `completed` tracks whether the task is already done (done tasks are
    skipped when building today's plan).
    """

    name: str
    category: str
    duration: int  # minutes
    priority: int
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def edit_task(self, task: Task) -> None:
        """Replace an existing task that has the same name as `task`.

        If no task with that name exists yet, the task is added instead.
        """
        for i, existing in enumerate(self.tasks):
            if existing.name == task.name:
                self.tasks[i] = task
                return
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove the task matching `task` (by name) from this pet."""
        self.tasks = [t for t in self.tasks if t.name != task.name]


@dataclass
class Owner:
    """A pet owner, their planning constraints, and their pets."""

    name: str
    available_minutes: int
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets.

        This is how the Scheduler reaches task data: it asks the Owner,
        and the Owner gathers tasks from each of its pets.
        """
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Builds and explains a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def make_plan(self) -> list[Task]:
        """Choose and order tasks that fit inside the owner's time budget.

        Strategy: take every not-yet-completed task, sort by priority
        (highest first, then shortest duration as a tiebreaker), then greedily
        include tasks while they still fit in `owner.available_minutes`.
        """
        candidates = [t for t in self.owner.all_tasks() if not t.completed]
        candidates.sort(key=lambda t: (-t.priority, t.duration))

        plan: list[Task] = []
        remaining = self.owner.available_minutes
        for task in candidates:
            if task.duration <= remaining:
                plan.append(task)
                remaining -= task.duration
        return plan

    def display_plan(self) -> str:
        """Return a readable "Today's Schedule" for the plan."""
        plan = self.make_plan()
        header = f"Today's Schedule for {self.owner.name}"
        lines = [header, "=" * len(header)]

        if not plan:
            lines.append("(No tasks fit in the available time.)")
            return "\n".join(lines)

        minute = DAY_START_HOUR * 60
        for task in plan:
            start = _format_clock(minute)
            lines.append(
                f"  {start}  {task.name} ({task.duration} min)"
                f"  [{_priority_label(task.priority)}] - {task.category}"
            )
            minute += task.duration

        used = sum(t.duration for t in plan)
        lines.append("")
        lines.append(
            f"Total: {len(plan)} task(s), {used} of "
            f"{self.owner.available_minutes} min used."
        )
        return "\n".join(lines)

    def explain(self) -> str:
        """Explain which tasks were scheduled or skipped, and why."""
        plan = self.make_plan()
        planned_ids = {id(t) for t in plan}
        lines = [f"Why this plan for {self.owner.name}:"]

        for task in self.owner.all_tasks():
            if task.completed:
                lines.append(f"  - {task.name}: skipped (already completed).")
            elif id(task) in planned_ids:
                lines.append(
                    f"  - {task.name}: scheduled "
                    f"({_priority_label(task.priority)} priority, "
                    f"{task.duration} min)."
                )
            else:
                lines.append(
                    f"  - {task.name}: skipped "
                    f"(no time left in the {self.owner.available_minutes}-min budget)."
                )
        return "\n".join(lines)


def _format_clock(total_minutes: int) -> str:
    """Convert an absolute minute-of-day into a HH:MM string."""
    hour, minute = divmod(total_minutes, 60)
    return f"{hour % 24:02d}:{minute:02d}"


def _priority_label(priority: int) -> str:
    """Map a priority int to a readable label."""
    return {3: "high", 2: "medium", 1: "low"}.get(priority, f"p{priority}")
