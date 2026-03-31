from pawpal_system import Task, Pet, Owner, AvailabilityBlock, Scheduler

# --- Owner ---
jordan = Owner(name="Jordan")
jordan.add_availability(AvailabilityBlock(label="Work", start_time="09:00", end_time="17:00", frequency="weekdays"))

# --- Pet 1: Mochi the dog ---
mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_care_task(Task(name="Morning Walk",   type="exercise",  priority="high",   duration=30, frequency="daily",  time_preference="morning"))
mochi.add_care_task(Task(name="Feeding",        type="nutrition", priority="high",   duration=10, frequency="daily",  time_preference="morning"))
mochi.add_care_task(Task(name="Evening Walk",   type="exercise",  priority="medium", duration=30, frequency="daily",  time_preference="evening"))
mochi.add_care_task(Task(name="Grooming",       type="hygiene",   priority="low",    duration=20, frequency="weekly", time_preference="afternoon"))

# --- Pet 2: Luna the cat ---
luna = Pet(name="Luna", species="cat", age=5)
luna.add_care_task(Task(name="Feeding",         type="nutrition", priority="high",   duration=10, frequency="daily",  time_preference="morning"))
luna.add_care_task(Task(name="Litter Box",      type="hygiene",   priority="medium", duration=10, frequency="daily",  time_preference="afternoon"))
luna.add_care_task(Task(name="Playtime",        type="enrichment",priority="low",    duration=15, frequency="daily",  time_preference="evening"))

# --- Build & display schedules ---
today = "2026-03-30"

print("=" * 50)
scheduler_mochi = Scheduler(owner=jordan, pet=mochi, date=today)
plan_mochi = scheduler_mochi.build_schedule()
plan_mochi.display()
print()
print(scheduler_mochi.explain_plan(plan_mochi))

print("\n" + "=" * 50)
scheduler_luna = Scheduler(owner=jordan, pet=luna, date=today)
plan_luna = scheduler_luna.build_schedule()
plan_luna.display()
print()
print(scheduler_luna.explain_plan(plan_luna))
