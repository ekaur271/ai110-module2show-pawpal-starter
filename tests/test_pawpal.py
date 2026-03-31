import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", type="exercise", priority="high", duration=30, frequency="daily")
    assert task.status == "incomplete"
    task.mark_complete()
    assert task.status == "complete"


def test_add_care_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.care_tasks) == 0
    pet.add_care_task(Task(name="Feeding", type="nutrition", priority="high", duration=10, frequency="daily"))
    assert len(pet.care_tasks) == 1
