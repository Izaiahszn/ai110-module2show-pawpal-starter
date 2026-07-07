"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant.
This is the "skeleton" generated from the UML diagram (diagram.mmd):
class names, attributes, and empty method stubs. No behavior yet —
implement the method bodies in the next step.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    """A pet owner and their planning constraints."""

    name: str
    available_minutes: int
    preferences: str = ""


@dataclass
class Task:
    """A single pet care task."""

    name: str
    category: str
    duration: int  # minutes
    priority: int


@dataclass
class Pet:
    """A pet and the tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        raise NotImplementedError

    def edit_task(self, task: Task) -> None:
        """Update an existing task on this pet."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        raise NotImplementedError


class Scheduler:
    """Builds and explains a care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def make_plan(self) -> list[Task]:
        """Choose and order tasks into a plan based on the owner's constraints."""
        raise NotImplementedError

    def display_plan(self) -> str:
        """Return a human-readable version of the plan."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why each task was chosen and when it happens."""
        raise NotImplementedError
