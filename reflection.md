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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
