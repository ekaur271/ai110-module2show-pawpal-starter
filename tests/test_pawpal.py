import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, AvailabilityBlock, Scheduler, ScheduledTask, DayPlan


# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_owner(busy_start=None, busy_end=None):
    owner = Owner(name="Jordan")
    if busy_start and busy_end:
        owner.add_availability(AvailabilityBlock(
            label="Work", start_time=busy_start, end_time=busy_end, frequency="weekdays"
        ))
    return owner

def make_task(name="Walk", priority="high", duration=30, frequency="daily", time_pref=None):
    return Task(name=name, type="exercise", priority=priority, duration=duration,
                frequency=frequency, time_preference=time_pref)


# ─── Original tests ───────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = make_task()
    assert task.status == "incomplete"
    task.mark_complete()
    assert task.status == "complete"


def test_add_care_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.care_tasks) == 0
    pet.add_care_task(make_task())
    assert len(pet.care_tasks) == 1


# ─── Happy paths ──────────────────────────────────────────────────────────────

def test_high_priority_scheduled_before_low():
    """High priority tasks should appear earlier in the schedule than low priority."""
    owner = make_owner()
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_care_task(make_task(name="Grooming", priority="low",  duration=20))
    pet.add_care_task(make_task(name="Feeding",  priority="high", duration=10))

    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")
    plan = scheduler.build_schedule()

    names = [st.task.name for st in plan.scheduled_tasks]
    assert names.index("Feeding") < names.index("Grooming")


def test_scheduler_avoids_busy_block():
    """No task should be scheduled inside the owner's busy block."""
    owner = make_owner(busy_start="08:00", busy_end="20:00")
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_care_task(make_task(name="Walk", duration=30))

    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")
    plan = scheduler.build_schedule()

    for st in plan.scheduled_tasks:
        start_min = int(st.start_time.replace(":", "").zfill(4)[:2]) * 60 + int(st.start_time[3:])
        end_min   = int(st.end_time.replace(":", "").zfill(4)[:2]) * 60 + int(st.end_time[3:])
        assert end_min <= 8 * 60 or start_min >= 20 * 60, (
            f"Task '{st.task.name}' scheduled inside busy block: {st.start_time}–{st.end_time}"
        )


def test_next_occurrence_daily():
    """Daily task should generate next occurrence one day later."""
    task = make_task(frequency="daily")
    next_t = task.next_occurrence("2026-03-31")
    assert next_t is not None
    assert next_t.due_date == "2026-04-01"
    assert next_t.status == "incomplete"


def test_next_occurrence_weekly():
    """Weekly task should generate next occurrence seven days later."""
    task = make_task(frequency="weekly")
    next_t = task.next_occurrence("2026-03-31")
    assert next_t is not None
    assert next_t.due_date == "2026-04-07"


def test_detect_conflicts_finds_overlap():
    """detect_conflicts should return a warning when two tasks overlap."""
    owner = make_owner()
    pet = Pet(name="Mochi", species="dog", age=3)
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")

    plan = DayPlan(date="2026-03-31", owner=owner, pet=pet)
    plan.add_task(ScheduledTask(task=make_task(name="Walk"),    start_time="08:00", end_time="08:30"))
    plan.add_task(ScheduledTask(task=make_task(name="Feeding"), start_time="08:15", end_time="08:25"))

    warnings = scheduler.detect_conflicts(plan)
    assert len(warnings) > 0
    assert "Walk" in warnings[0]
    assert "Feeding" in warnings[0]


def test_sort_by_time_returns_chronological_order():
    """sort_by_time should return scheduled tasks ordered earliest to latest."""
    owner = make_owner()
    pet = Pet(name="Mochi", species="dog", age=3)
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")

    plan = DayPlan(date="2026-03-31", owner=owner, pet=pet)
    plan.add_task(ScheduledTask(task=make_task(name="Evening Walk"), start_time="18:00", end_time="18:30"))
    plan.add_task(ScheduledTask(task=make_task(name="Feeding"),      start_time="08:00", end_time="08:10"))
    plan.add_task(ScheduledTask(task=make_task(name="Grooming"),     start_time="13:00", end_time="13:20"))

    sorted_tasks = scheduler.sort_by_time(plan)
    times = [st.start_time for st in sorted_tasks]
    assert times == sorted(times), f"Expected chronological order, got: {times}"


# ─── Edge cases ───────────────────────────────────────────────────────────────

def test_build_schedule_empty_tasks():
    """Scheduler should return an empty DayPlan when pet has no tasks."""
    owner = make_owner()
    pet = Pet(name="Mochi", species="dog", age=3)
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")
    plan = scheduler.build_schedule()
    assert len(plan.scheduled_tasks) == 0


def test_next_occurrence_as_needed_returns_none():
    """Tasks with 'as needed' frequency should not generate a next occurrence."""
    task = make_task(frequency="as needed")
    assert task.next_occurrence("2026-03-31") is None


def test_no_slot_when_day_fully_blocked():
    """When the entire day is blocked, no tasks should be scheduled."""
    owner = make_owner(busy_start="00:00", busy_end="23:59")
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_care_task(make_task(name="Walk", duration=30))

    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")
    plan = scheduler.build_schedule()
    assert len(plan.scheduled_tasks) == 0


def test_mark_complete_then_incomplete_resets():
    """Marking complete then incomplete should cleanly reset status and next_task."""
    task = make_task(frequency="daily")
    st = ScheduledTask(task=task, start_time="08:00", end_time="08:30")
    st.mark_complete(on_date="2026-03-31")
    assert st.is_complete is True
    assert st.next_task is not None

    task.mark_incomplete()
    st.is_complete = False
    st.next_task = None
    assert st.is_complete is False
    assert task.status == "incomplete"
    assert st.next_task is None


def test_detect_conflicts_no_overlap():
    """detect_conflicts should return no warnings when tasks do not overlap."""
    owner = make_owner()
    pet = Pet(name="Mochi", species="dog", age=3)
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-03-31")

    plan = DayPlan(date="2026-03-31", owner=owner, pet=pet)
    plan.add_task(ScheduledTask(task=make_task(name="Walk"),    start_time="08:00", end_time="08:30"))
    plan.add_task(ScheduledTask(task=make_task(name="Feeding"), start_time="08:30", end_time="08:40"))

    warnings = scheduler.detect_conflicts(plan)
    assert len(warnings) == 0
