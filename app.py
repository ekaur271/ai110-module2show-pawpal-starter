import streamlit as st
from pawpal_system import Owner, Pet, Task, AvailabilityBlock, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = []

# --- Section 1: Owner Setup ---
st.subheader("Owner Setup")

owner_name = st.text_input("Owner name", value="Jordan")

if st.button("Set Owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.session_state.pets = []
    st.success(f"Owner '{owner_name}' created!")

if st.session_state.owner:
    st.caption(f"Current owner: **{st.session_state.owner.name}**")

st.divider()

# --- Section 2: Add a Pet ---
st.subheader("Register a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Please set an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species, age=age)
        st.session_state.pets.append(new_pet)
        st.success(f"Pet '{pet_name}' added!")

if st.session_state.pets:
    st.caption("Registered pets: " + ", ".join(p.name for p in st.session_state.pets))

st.divider()

# --- Section 3: Add Tasks to a Pet ---
st.subheader("Add Care Tasks")

if not st.session_state.pets:
    st.info("Add a pet above before adding tasks.")
else:
    selected_pet_name = st.selectbox("Select pet", [p.name for p in st.session_state.pets])
    selected_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_name = st.text_input("Task name", value="Morning Walk")
    with col2:
        task_type = st.selectbox("Type", ["exercise", "nutrition", "hygiene", "enrichment", "medication"])
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"])

    col4, col5 = st.columns(2)
    with col4:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col5:
        time_pref = st.selectbox("Time preference", ["morning", "afternoon", "evening", "none"])

    if st.button("Add Task"):
        task = Task(
            name=task_name,
            type=task_type,
            priority=priority,
            duration=int(duration),
            frequency="daily",
            time_preference=None if time_pref == "none" else time_pref
        )
        selected_pet.add_care_task(task)   # <-- Pet.add_care_task() handles this
        st.success(f"Task '{task_name}' added to {selected_pet.name}!")

    if selected_pet.get_all_tasks():
        st.write(f"Tasks for **{selected_pet.name}**:")
        st.table([
            {"Task": t.name, "Type": t.type, "Priority": t.priority, "Duration (min)": t.duration, "Time Pref": t.time_preference or "any"}
            for t in selected_pet.get_all_tasks()
        ])

st.divider()

# --- Section 4: Generate Schedule ---
st.subheader("Generate Schedule")

if not st.session_state.pets:
    st.info("Add a pet and tasks before generating a schedule.")
else:
    schedule_pet_name = st.selectbox("Select pet to schedule", [p.name for p in st.session_state.pets], key="schedule_pet")
    schedule_pet = next(p for p in st.session_state.pets if p.name == schedule_pet_name)

    col_start, col_end = st.columns(2)
    with col_start:
        day_start = st.text_input("Day start (HH:MM)", value="08:00")
    with col_end:
        day_end = st.text_input("Day end (HH:MM)", value="22:00")

    if st.button("Generate Schedule"):
        if not schedule_pet.get_all_tasks():
            st.warning(f"No tasks added for {schedule_pet.name} yet.")
        else:
            scheduler = Scheduler(
                owner=st.session_state.owner,
                pet=schedule_pet,
                date="today",
                day_start=day_start,
                day_end=day_end
            )
            plan = scheduler.build_schedule()        # <-- Scheduler.build_schedule() handles this

            st.success("Schedule generated!")
            st.markdown(f"### {schedule_pet.name}'s Day Plan")

            for st_task in plan.scheduled_tasks:
                st.markdown(f"- **{st_task.start_time}–{st_task.end_time}** — {st_task.task.name} ({st_task.task.priority} priority)")

            status = plan.get_completion_status()
            st.caption(f"{status['complete']}/{status['total']} tasks complete")

            st.markdown("#### Why this schedule?")
            st.text(scheduler.explain_plan(plan))
