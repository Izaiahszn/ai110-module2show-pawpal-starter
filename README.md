# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Owner / Pet / Task model** — an owner keeps a list of pets, each pet keeps its own
  list of care tasks (`Owner`, `Pet`, `Task` in `pawpal_system.py`).
- **Priority-based day planning** — `Scheduler.make_plan()` picks the highest-priority
  tasks (shortest duration breaks ties) and greedily fits them into the owner's
  available minutes; `display_plan()` lays them out as a timeline and `explain()` says
  why each task was scheduled or skipped.
- **Sorting by time** — `Scheduler.sort_by_time()` orders tasks by their "HH:MM" time
  (untimed tasks last), so the task list reads like a daily timeline.
- **Filtering** — `Scheduler.filter_tasks(pet_name, completed)` filters by pet, by
  completion status, both, or neither.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any pending tasks booked
  at the exact same time and returns friendly warning strings (it never crashes).
- **Daily / weekly recurrence** — completing a recurring task
  (`Scheduler.mark_task_complete()` → `Pet.complete_task()` → `Task.next_occurrence()`)
  automatically creates the next instance with its `due_date` advanced via `timedelta`.
- **Streamlit UI** — add pets and tasks, see the sorted task table and live conflict
  warnings, and generate a plan; state persists across reruns via `st.session_state`.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Terminal output from running the CLI demo (`python main.py`), which exercises the
smarter-scheduling features (sorting, filtering, conflict detection, recurring tasks):

```
=== All tasks, sorted by time ===
  07:30  Feeding (10 min)
  08:00  Morning walk (30 min)
  08:00  Vet meds (5 min)
  12:00  Midday play (20 min)
  18:00  Evening walk (30 min)

=== Filter: only Mochi's tasks ===
  Evening walk @ 18:00
  Morning walk @ 08:00
  Midday play @ 12:00

=== Conflict detection ===
  WARNING - conflict at 08:00: Morning walk, Vet meds

=== Recurring task ===
  Completed 'Morning walk' (daily). Next occurrence due: 2026-07-08

=== Filter: pending (not completed) tasks ===
  Evening walk @ 18:00 (due None)
  Midday play @ 12:00 (due None)
  Morning walk @ 08:00 (due 2026-07-08)
  Feeding @ 07:30 (due None)
  Vet meds @ 08:00 (due None)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
collected 2 items

tests\test_pawpal.py ..                                                  [100%]

============================== 2 passed in 0.07s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their "HH:MM" time; untimed tasks go last. Also `make_plan()` sorts by priority (duration as tiebreaker). |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filter by pet name and/or completion status; either argument is optional. |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight: warns when pending tasks share the **exact same** start time (returns messages, never raises). |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()`, `Scheduler.mark_task_complete()` | Completing a "daily"/"weekly" task auto-creates the next instance with `due_date` advanced via `timedelta`. |

## 🎬 Demo Walkthrough

### What the UI lets you do

Run the app with `streamlit run app.py`. The page is a single scrolling form:

- **Owner** — set the owner's name, minutes available today, and preferences.
- **Add a pet** — enter a name + species; the pet is stored on the `Owner` and persists
  across reruns via `st.session_state`.
- **Add a task** — choose the pet, then give the task a title, category, duration,
  priority, **time**, and **frequency** (once / daily / weekly).
- **Current tasks** — a table sorted by time (via `Scheduler.sort_by_time()`), with any
  double-booked time slots surfaced as live conflict warnings.
- **Build Schedule** — generates today's plan and an explanation of why each task was
  chosen or skipped.

### Example workflow

1. Enter the owner (e.g. *Jordan*, 60 minutes available).
2. **Add a pet:** *Mochi* the dog.
3. **Add a task:** *Morning walk*, exercise, 20 min, high priority, 08:00, daily.
4. **Add another task at the same time:** *Vet meds*, health, 08:00 — the app now shows a
   conflict warning: `WARNING - conflict at 08:00: Morning walk, Vet meds`.
5. Click **Generate schedule** to see today's plan and the reasoning behind it.

### Key Scheduler behaviors shown

- **Sorting** — the task table is ordered by time, not insertion order.
- **Conflict warnings** — same-time tasks are flagged before you commit to a plan.
- **Priority planning** — `make_plan()` fits the most important tasks into the budget.
- **Recurrence** — completing the daily *Morning walk* schedules the next day's instance.

### Sample CLI output (`python main.py`)

```
=== All tasks, sorted by time ===
  07:30  Feeding (10 min)
  08:00  Morning walk (30 min)
  08:00  Vet meds (5 min)
  12:00  Midday play (20 min)
  18:00  Evening walk (30 min)

=== Filter: only Mochi's tasks ===
  Evening walk @ 18:00
  Morning walk @ 08:00
  Midday play @ 12:00

=== Conflict detection ===
  WARNING - conflict at 08:00: Morning walk, Vet meds

=== Recurring task ===
  Completed 'Morning walk' (daily). Next occurrence due: 2026-07-08

=== Filter: pending (not completed) tasks ===
  Evening walk @ 18:00 (due None)
  Midday play @ 12:00 (due None)
  Morning walk @ 08:00 (due 2026-07-08)
  Feeding @ 07:30 (due None)
  Vet meds @ 08:00 (due None)
```

The UML for the final system lives in [`diagrams/uml_final.mmd`](diagrams/uml_final.mmd).
