from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, time, date, timedelta


def parse_time(t: str) -> time:
    """Parse a time string in HH:MM format into a time object."""
    return datetime.strptime(t, "%H:%M").time()

def minutes_to_time(minutes: int) -> str:
    """Convert total minutes since midnight to a HH:MM string."""
    h, m = divmod(minutes, 60)
    return f"{h:02d}:{m:02d}"

def time_to_minutes(t: str) -> int:
    """Convert a HH:MM string to total minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m


@dataclass
class Task:
    name: str
    type: str
    priority: str          # "high", "medium", "low"
    duration: int          # minutes
    frequency: str         # "daily", "weekly", etc.
    time_preference: Optional[str] = None   # "morning", "afternoon", "evening"
    status: str = "incomplete"
    due_date: Optional[str] = None          # "YYYY-MM-DD", set when task is scheduled

    def assign_priority(self, priority: str):
        """Set the priority level of this task."""
        self.priority = priority

    def assign_duration(self, duration: int):
        """Set how long this task takes in minutes."""
        self.duration = duration

    def assign_frequency(self, frequency: str):
        """Set how often this task recurs."""
        self.frequency = frequency

    def assign_time_preference(self, time_preference: str):
        """Set the preferred time of day for this task."""
        self.time_preference = time_preference

    def mark_complete(self):
        """Mark this task as complete."""
        self.status = "complete"

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.status = "incomplete"

    def next_occurrence(self, from_date: str) -> Optional["Task"]:
        """Return a new incomplete Task instance due on the next occurrence based on frequency."""
        FREQUENCY_DELTAS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        delta = FREQUENCY_DELTAS.get(self.frequency)
        if delta is None:
            return None
        next_date = datetime.strptime(from_date, "%Y-%m-%d").date() + delta
        return Task(
            name=self.name,
            type=self.type,
            priority=self.priority,
            duration=self.duration,
            frequency=self.frequency,
            time_preference=self.time_preference,
            status="incomplete",
            due_date=str(next_date)
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_tasks: List[Task] = field(default_factory=list)

    def add_care_task(self, task: Task):
        """Add a care task to this pet's task list."""
        self.care_tasks.append(task)

    def remove_care_task(self, task: Task):
        """Remove a care task from this pet's task list."""
        self.care_tasks.remove(task)

    def get_all_tasks(self) -> List[Task]:
        """Return all care tasks for this pet."""
        return self.care_tasks

    def update_age(self, age: int):
        """Update the pet's age."""
        self.age = age


@dataclass
class AvailabilityBlock:
    label: str
    start_time: str        # e.g. "09:00"
    end_time: str          # e.g. "17:00"
    frequency: str         # "daily", "weekdays", etc.

    def update_start(self, start_time: str):
        """Update the start time of this availability block."""
        self.start_time = start_time

    def update_end(self, end_time: str):
        """Update the end time of this availability block."""
        self.end_time = end_time

    def add_frequency(self, frequency: str):
        """Set how often this block recurs."""
        self.frequency = frequency

    def conflicts_with(self, start_time: str, end_time: str) -> bool:
        """Return True if the given time slot overlaps with this busy block."""
        block_start = time_to_minutes(self.start_time)
        block_end = time_to_minutes(self.end_time)
        slot_start = time_to_minutes(start_time)
        slot_end = time_to_minutes(end_time)
        return not (slot_end <= block_start or slot_start >= block_end)


@dataclass
class Owner:
    name: str
    availability: List[AvailabilityBlock] = field(default_factory=list)

    def add_availability(self, block: AvailabilityBlock):
        """Add a busy time block to the owner's schedule."""
        self.availability.append(block)

    def get_free_slots(self) -> List[AvailabilityBlock]:
        """Return all availability blocks for this owner."""
        return self.availability


@dataclass
class ScheduledTask:
    task: Task
    start_time: str        # e.g. "08:00"
    end_time: str          # e.g. "08:30"
    is_complete: bool = False
    next_task: Optional["Task"] = field(default=None, repr=False)

    def mark_complete(self, on_date: Optional[str] = None):
        """Mark this scheduled task complete and generate the next occurrence if recurring."""
        self.is_complete = True
        self.task.mark_complete()
        if on_date:
            self.next_task = self.task.next_occurrence(on_date)

    def update_start(self, start_time: str):
        """Update the scheduled start time."""
        self.start_time = start_time

    def update_finish(self, end_time: str):
        """Update the scheduled end time."""
        self.end_time = end_time


class DayPlan:
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks: List[ScheduledTask] = []

    def add_task(self, scheduled_task: ScheduledTask):
        """Append a scheduled task to today's plan."""
        self.scheduled_tasks.append(scheduled_task)

    def get_completion_status(self) -> dict:
        """Return a summary dict with total, complete, and remaining task counts."""
        total = len(self.scheduled_tasks)
        complete = sum(1 for st in self.scheduled_tasks if st.is_complete)
        return {"total": total, "complete": complete, "remaining": total - complete}

    def filter_tasks(self, status: str = "all") -> List[ScheduledTask]:
        """Return scheduled tasks filtered by completion status: 'complete', 'incomplete', or 'all'."""
        if status == "complete":
            return [st for st in self.scheduled_tasks if st.is_complete]
        elif status == "incomplete":
            return [st for st in self.scheduled_tasks if not st.is_complete]
        return self.scheduled_tasks

    def display(self):
        """Print the day's schedule and completion status to the terminal."""
        print(f"\n--- DayPlan for {self.pet.name} on {self.date} ---")
        print(f"Owner: {self.owner.name}")
        for st in self.scheduled_tasks:
            status = "✓" if st.is_complete else "○"
            print(f"  [{status}] {st.start_time}–{st.end_time}  {st.task.name} ({st.task.priority} priority)")
        status = self.get_completion_status()
        print(f"\n{status['complete']}/{status['total']} tasks complete")


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

TIME_PREF_WINDOWS = {
    "morning":   ("08:00", "12:00"),
    "afternoon": ("12:00", "17:00"),
    "evening":   ("17:00", "22:00"),
}


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, date: str, day_start: str = "08:00", day_end: str = "22:00"):
        self.owner = owner
        self.pet = pet
        self.date = date
        self.day_start = day_start
        self.day_end = day_end
        self._scheduled_slots: List[tuple] = []  # list of (start_min, end_min) already booked

    def build_schedule(self) -> DayPlan:
        """Build and return a DayPlan by prioritizing and slotting all pet tasks."""
        plan = DayPlan(self.date, self.owner, self.pet)
        tasks = self.prioritize_tasks(self.pet.get_all_tasks())
        for task in tasks:
            slot = self.find_available_slot(task.duration, task.time_preference)
            if slot:
                start = slot
                end_min = time_to_minutes(start) + task.duration
                end = minutes_to_time(end_min)
                scheduled = ScheduledTask(task=task, start_time=start, end_time=end)
                plan.add_task(scheduled)
                self._scheduled_slots.append((time_to_minutes(start), end_min))
        return plan

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks from highest to lowest priority."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

    def find_available_slot(self, duration: int, time_preference: Optional[str] = None) -> Optional[str]:
        """Find the earliest open time slot of the given duration, respecting owner availability and time preference."""
        day_start_min = time_to_minutes(self.day_start)
        day_end_min = time_to_minutes(self.day_end)

        if time_preference and time_preference in TIME_PREF_WINDOWS:
            pref_start, pref_end = TIME_PREF_WINDOWS[time_preference]
            search_start = max(day_start_min, time_to_minutes(pref_start))
            search_end = min(day_end_min, time_to_minutes(pref_end))
        else:
            search_start = day_start_min
            search_end = day_end_min

        current = search_start
        while current + duration <= search_end:
            candidate_end = current + duration
            candidate_start_str = minutes_to_time(current)
            candidate_end_str = minutes_to_time(candidate_end)

            blocked_by_owner = any(
                block.conflicts_with(candidate_start_str, candidate_end_str)
                for block in self.owner.availability
            )
            blocked_by_scheduled = any(
                not (candidate_end <= s or current >= e)
                for s, e in self._scheduled_slots
            )

            if not blocked_by_owner and not blocked_by_scheduled:
                return candidate_start_str

            current += 15

        return None

    def detect_conflicts(self, *plans: DayPlan) -> List[str]:
        """Check one or more DayPlans for overlapping task times and return warning messages."""
        warnings = []
        all_scheduled = []
        for plan in plans:
            for st in plan.scheduled_tasks:
                all_scheduled.append((plan.pet.name, st))

        for i in range(len(all_scheduled)):
            pet_a, task_a = all_scheduled[i]
            for j in range(i + 1, len(all_scheduled)):
                pet_b, task_b = all_scheduled[j]
                a_start = time_to_minutes(task_a.start_time)
                a_end   = time_to_minutes(task_a.end_time)
                b_start = time_to_minutes(task_b.start_time)
                b_end   = time_to_minutes(task_b.end_time)
                if not (a_end <= b_start or b_end <= a_start):
                    warnings.append(
                        f"⚠ CONFLICT: '{task_a.task.name}' ({pet_a}, {task_a.start_time}–{task_a.end_time}) "
                        f"overlaps with '{task_b.task.name}' ({pet_b}, {task_b.start_time}–{task_b.end_time})"
                    )
        return warnings

    def sort_by_time(self, plan: DayPlan) -> List[ScheduledTask]:
        """Return the plan's scheduled tasks sorted by start time (earliest first)."""
        return sorted(plan.scheduled_tasks, key=lambda st: time_to_minutes(st.start_time))

    def explain_plan(self, plan: DayPlan) -> str:
        """Return a human-readable explanation of why each task was scheduled when it was."""
        lines = [f"Schedule for {plan.pet.name} on {plan.date}:\n"]
        for st in plan.scheduled_tasks:
            pref = f" (prefers {st.task.time_preference})" if st.task.time_preference else ""
            lines.append(
                f"• {st.task.name} at {st.start_time}–{st.end_time} "
                f"— {st.task.priority} priority, {st.task.duration} min{pref}"
            )
        if not plan.scheduled_tasks:
            lines.append("No tasks could be scheduled — check availability blocks or task durations.")
        return "\n".join(lines)
