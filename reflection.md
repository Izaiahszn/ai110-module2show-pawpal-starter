# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

The Owner and each Pet each have their own "profile" of information. Those feed into
the Scheduler, which looks at what the owner has time for and what the pets need, and
produces a daily plan showing what happens and when.

- What classes did you include, and what responsibilities did you assign to each?

I used four classes:

- **Owner** — holds the owner's info and planning constraints: `name`,
  `available_minutes`, and `preferences`. This is the "how much time / what do they
  care about" side of the plan.
- **Pet** — holds a pet's `name` and `species` plus its `list[Task]`. It is
  responsible for managing its own tasks with `add_task`, `edit_task`, and
  `remove_task`.
- **Task** — a single care task: `name`, `category`, `duration` (minutes), and
  `priority`. Pure data, so I made it a dataclass.
- **Scheduler** — plans for an Owner. `make_plan()` builds the daily plan from the
  constraints and task priorities, `display_plan()` shows it clearly, and `explain()`
  says why each task was scheduled or skipped.

I made Owner, Pet, and Task dataclasses because they mostly hold data, and kept
Scheduler a regular class because it holds behavior (the planning logic) rather than
data.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. When I asked my AI assistant to review the skeleton, it caught a missing
relationship: my UML said Owner "1" → "*" Pet, but nothing in the code actually held
the pets. The `Owner` class had no `pets` attribute and the `Scheduler` only stored
`owner`, so `make_plan()` had no way to reach any `Task` (tasks live on `Pet.tasks`).
I added a `pets: list[Pet]` field to `Owner` so the Scheduler can walk
`owner.pets` → each pet's tasks and actually build a plan.

The review also flagged issues I'm noting for later: `edit_task`/`remove_task` can't
tell two identical tasks apart without a unique id, `priority` as an int needs a clear
convention (and my Streamlit UI uses "low/medium/high" strings, which I'll need to
reconcile), and the returned plan has no start times even though `explain()` is meant
to say *when* tasks happen. I left those as-is for now and only fixed the Owner→Pet
link, since that one blocked the scheduler from working at all.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers the owner's total available minutes (a time budget), each
task's priority (higher int = more important), each task's duration, and whether a
task is already completed. Tasks also carry a scheduled time ("HH:MM") and a
frequency ("once"/"daily"/"weekly").

- How did you decide which constraints mattered most?

Time budget and priority mattered most, because the core problem is "the owner only
has so many minutes, so do the most important things first." `make_plan()` sorts by
priority (shortest duration as a tiebreaker) and greedily fills the budget. Scheduled
time is used for sorting and conflict detection rather than for the budget itself.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict detection (`Scheduler.detect_conflicts()`) only flags tasks that share the
**exact same start time** ("HH:MM"). It does not account for overlapping durations —
e.g. a 30-minute task at 08:00 and another at 08:15 overlap in real life, but my code
does not warn about that. I chose exact-match because it is simple, fast (one pass,
grouping by time string), and easy to read, and it catches the most common mistake:
double-booking the same slot. For a lightweight pet-care helper that is a reasonable
tradeoff; true interval-overlap detection (comparing start + duration ranges) would be
the next improvement if the app needed it.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI across every phase: generating the class skeletons from my UML, implementing
the method bodies, brainstorming the "smarter scheduling" algorithms (sorting,
filtering, recurrence, conflict detection), and debugging. The most effective features
were **agent/automatic editing** (it could edit `pawpal_system.py`, `main.py`, and
`app.py` together for a change like recurring tasks) and **inline chat on a specific
method** to ask focused questions.

- What kinds of prompts or questions were most helpful?

Specific, code-anchored questions worked best — e.g. "Based on my skeletons, how should
the Scheduler retrieve all tasks from the Owner's pets?" (which led to `Owner.all_tasks()`)
and "How do I sort tasks in HH:MM format using a lambda key?" Vague prompts gave vague
answers; attaching the actual file and naming the method gave usable ones.

- Which AI features were most effective for building the scheduler?

Multi-file agent edits (for the recurrence change that touched `Task`, `Pet`, and the
demo) and running my code through a headless test harness to *verify* behavior instead
of trusting the explanation.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

Two examples. (1) The AI first wrote conflict warnings with a ⚠️ emoji prefix; it
crashed on the Windows terminal (`cp1252` can't encode it), so I changed it to a plain
`"WARNING - conflict at ..."` string that runs anywhere. (2) When asked to "simplify"
the `sort_by_time` key, a denser one-liner was suggested, but I kept the explicit
`lambda t: (t.time == "", t.time)` because its intent (untimed tasks last, then
chronological) is easier for a human to read.

- How did you evaluate or verify what the AI suggested?

I didn't trust output text — I ran it. `python main.py` exercised every feature in the
terminal, and I drove the Streamlit UI through a headless test to confirm that adding a
pet, adding two same-time tasks, and generating a schedule actually produced the right
objects and the conflict warning. I also kept the `pytest` suite green after each change.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

Automated `pytest` tests cover two core behaviors: `Task.mark_complete()` flips a task's
status to completed, and `Pet.add_task()` increases that pet's task count. Beyond the
unit tests, I verified the scheduling features end-to-end by running `main.py`
(sorting, filtering, conflict detection, recurrence) and by driving the Streamlit UI
headlessly (add pet → add conflicting tasks → generate schedule).

- Why were these tests important?

They cover the two operations everything else depends on: if completing or adding tasks
were broken, the plan, recurrence, and conflict logic would all be wrong.

**b. Confidence**

- How confident are you that your scheduler works correctly?

Fairly confident for the common cases — the plan, sorting, filtering, conflicts, and
recurrence all behave correctly in the demo and headless UI runs. My confidence is
lower on unusual inputs, because those aren't covered by automated tests yet.

- What edge cases would you test next if you had more time?

Overlapping-duration conflicts (not just exact-time matches), an empty or tiny time
budget, tasks with a malformed or missing time string, duplicate task names within a
pet, and completing a recurring task many times in a row.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The clean separation between the logic layer (`pawpal_system.py`) and the UI (`app.py`).
Because the Scheduler was built and verified CLI-first, wiring it into Streamlit was
mostly about calling existing methods, and the "smart" features (sorting, conflict
warnings) dropped straight into the UI.

- How did using separate chat sessions for different phases help you stay organized?

Keeping a separate chat for algorithm planning vs. core implementation stopped the
context from getting muddled — the planning session could brainstorm freely without the
assistant trying to immediately rewrite my working files, and each session stayed
focused on one concern.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd make `make_plan()` honor each task's actual `time` (right now it schedules by
priority/budget and lays tasks out sequentially from 08:00, separate from the `time`
field used for sorting and conflicts), and upgrade conflict detection from exact-time
matches to real interval overlap. I'd also give tasks a stable id so edit/remove don't
rely on matching by name.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Being the "lead architect" means the AI is fast at producing code, but the design
decisions and verification are mine. The AI could generate a scheduler in seconds, yet I
was the one who caught the missing Owner→Pet link, chose the priority convention, decided
the exact-match conflict tradeoff, and *ran* the code to confirm it worked. Powerful AI
raises the value of judgment, not lowers it — my job was to direct it and check its work,
not to accept it blindly.
