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

## Smarter Scheduling

PawPal+ goes beyond a basic task list with several intelligent scheduling features:

- **Priority-based scheduling** — tasks are sorted high → medium → low before being placed, so critical needs like feeding and medication always get a slot first.
- **Availability-aware slot finding** — the scheduler scans the day in 15-minute increments and skips any window that overlaps with the owner's busy blocks (e.g. a 9–5 work schedule).
- **Time preference windows** — tasks can specify morning (8–12), afternoon (12–17), or evening (17–22), and the scheduler searches within that window first.
- **Conflict detection** — after building schedules for multiple pets, the app automatically checks for overlapping task times and surfaces warnings.
- **Recurring task generation** — when a daily or weekly task is marked complete, a new instance is automatically created with the next due date using Python's `timedelta`.
- **Sorting and filtering** — the task list can be filtered by type and sorted by priority, duration, or name; the schedule view can be sorted by time or priority.

## Testing PawPal+

```bash
python -m pytest tests/test_pawpal.py -v
```

The test suite covers 12 behaviors across happy paths and edge cases:

- **Task completion** — marking a task complete changes its status, and marking it incomplete resets it cleanly
- **Pet task management** — adding a task to a pet correctly increases its task count
- **Priority ordering** — the scheduler always places high priority tasks before low priority ones
- **Availability conflict avoidance** — no task gets scheduled inside the owner's busy block
- **Sorting correctness** — `sort_by_time` returns tasks in chronological order regardless of input order
- **Recurrence logic** — daily tasks generate a next occurrence for the following day, weekly for 7 days out, and "as needed" tasks return nothing
- **Conflict detection** — overlapping tasks are flagged with a warning; back-to-back tasks are not
- **Edge cases** — empty pet task list, fully blocked day, and resetting completion state all behave correctly

**Confidence level: ⭐⭐⭐⭐ (4/5)**

The core scheduling logic, priority system, and recurring tasks are well tested and reliable. I'd give it a 5 if I had tests covering the time preference windows more thoroughly and multi-pet conflict detection across separate plans.

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
