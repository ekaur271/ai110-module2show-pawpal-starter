from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    type: str
    priority: str          # "high", "medium", "low"
    duration: int          # minutes
    frequency: str         # "daily", "weekly", etc.
    time_preference: Optional[str] = None   # "morning", "afternoon", "evening"
    status: str = "incomplete"

    def assign_priority(self, priority: str):
        pass

    def assign_duration(self, duration: int):
        pass

    def assign_frequency(self, frequency: str):
        pass

    def assign_time_preference(self, time_preference: str):
        pass

    def mark_complete(self):
        pass

    def mark_incomplete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_tasks: List[Task] = field(default_factory=list)

    def add_care_task(self, task: Task):
        pass

    def remove_care_task(self, task: Task):
        pass

    def get_all_tasks(self) -> List[Task]:
        pass

    def update_age(self, age: int):
        pass


@dataclass
class AvailabilityBlock:
    label: str
    start_time: str        # e.g. "09:00"
    end_time: str          # e.g. "17:00"
    frequency: str         # "daily", "weekdays", etc.

    def update_start(self, start_time: str):
        pass

    def update_end(self, end_time: str):
        pass

    def add_frequency(self, frequency: str):
        pass

    def conflicts_with(self, start_time: str, end_time: str) -> bool:
        pass


@dataclass
class Owner:
    name: str
    availability: List[AvailabilityBlock] = field(default_factory=list)

    def add_availability(self, block: AvailabilityBlock):
        pass

    def get_free_slots(self) -> List[AvailabilityBlock]:
        pass


@dataclass
class ScheduledTask:
    task: Task
    start_time: str        # e.g. "08:00"
    end_time: str          # e.g. "08:30"
    is_complete: bool = False

    def mark_complete(self):
        pass

    def update_start(self, start_time: str):
        pass

    def update_finish(self, end_time: str):
        pass


class DayPlan:
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks: List[ScheduledTask] = []

    def add_task(self, scheduled_task: ScheduledTask):
        pass

    def get_completion_status(self) -> dict:
        pass

    def display(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, date: str, day_start: str = "08:00", day_end: str = "22:00"):
        self.owner = owner
        self.pet = pet
        self.date = date
        self.day_start = day_start
        self.day_end = day_end

    def build_schedule(self) -> DayPlan:
        pass

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def find_available_slot(self, duration: int) -> Optional[str]:
        pass

    def explain_plan(self, plan: DayPlan) -> str:
        pass
