import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, AvailabilityBlock, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

TODAY = str(date.today())
PRIORITY_BADGE = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# ─── Session State ───────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "plans" not in st.session_state:
    st.session_state.plans = {}

# ─── Header ──────────────────────────────────────────────────────────────────
st.title("🐾 PawPal+")
st.caption("Your smart pet care scheduler.")

if st.session_state.owner:
    st.info(
        f"👤 **{st.session_state.owner.name}** · "
        f"{len(st.session_state.pets)} pet(s) · "
        f"Today: {TODAY}",
        icon=None
    )

tab1, tab2, tab3, tab4 = st.tabs(["👤 Owner", "🐾 Pets", "📋 Tasks", "📅 Schedule"])


# ─────────────────────────────────────────────
# TAB 1: OWNER
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Owner Setup")

    owner_name = st.text_input("Your name", value="Jordan")
    if st.button("Set Owner", type="primary"):
        st.session_state.owner = Owner(name=owner_name)
        st.session_state.pets = []
        st.session_state.plans = {}
        st.success(f"Welcome, {owner_name}!")
        st.rerun()

    if st.session_state.owner is None:
        st.info("Set your name above to get started.")
    else:
        st.divider()
        st.subheader("⛔ Busy Time Blocks")
        st.caption("The scheduler will work around these times.")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            block_label = st.text_input("Label", value="Work")
        with col2:
            block_start = st.text_input("Start (HH:MM)", value="09:00")
        with col3:
            block_end = st.text_input("End (HH:MM)", value="17:00")
        with col4:
            block_freq = st.selectbox("Frequency", ["weekdays", "daily", "weekends"])

        if st.button("Add Busy Block"):
            st.session_state.owner.add_availability(
                AvailabilityBlock(label=block_label, start_time=block_start, end_time=block_end, frequency=block_freq)
            )
            st.success(f"Added: {block_label} ({block_start}–{block_end})")
            st.rerun()

        if st.session_state.owner.availability:
            for i, b in enumerate(st.session_state.owner.availability):
                col_b, col_del = st.columns([5, 1])
                with col_b:
                    st.markdown(f"⛔ **{b.label}** · {b.start_time}–{b.end_time} · _{b.frequency}_")
                with col_del:
                    if st.button("✕", key=f"del_block_{i}", help="Remove this block"):
                        st.session_state.owner.availability.pop(i)
                        st.rerun()
        else:
            st.caption("No busy blocks added yet — scheduler will use the full day.")


# ─────────────────────────────────────────────
# TAB 2: PETS
# ─────────────────────────────────────────────
with tab2:
    if st.session_state.owner is None:
        st.warning("Set up your owner profile in the **Owner** tab first.")
    else:
        st.subheader("Register a Pet")
        col1, col2, col3 = st.columns(3)
        with col1:
            pet_name = st.text_input("Pet name", value="Mochi")
        with col2:
            species = st.selectbox("Species", ["dog", "cat", "other"])
        with col3:
            age = st.number_input("Age", min_value=0, max_value=30, value=2)

        if st.button("Add Pet", type="primary"):
            if pet_name in [p.name for p in st.session_state.pets]:
                st.warning(f"A pet named '{pet_name}' already exists.")
            else:
                st.session_state.pets.append(Pet(name=pet_name, species=species, age=age))
                st.success(f"{pet_name} registered!")
                st.rerun()

        if st.session_state.pets:
            st.divider()
            st.subheader("Your Pets")
            for i, pet in enumerate(st.session_state.pets):
                species_icon = {"dog": "🐕", "cat": "🐈"}.get(pet.species, "🐾")
                col_info, col_del = st.columns([5, 1])
                with col_info:
                    st.markdown(f"{species_icon} **{pet.name}** · {pet.species} · age {pet.age} · {len(pet.care_tasks)} task(s)")
                with col_del:
                    if st.button("✕", key=f"del_pet_{i}", help=f"Remove {pet.name}"):
                        st.session_state.pets.pop(i)
                        st.session_state.plans.pop(pet.name, None)
                        st.rerun()


# ─────────────────────────────────────────────
# TAB 3: TASKS
# ─────────────────────────────────────────────
with tab3:
    if not st.session_state.pets:
        st.warning("Add a pet in the **Pets** tab first.")
    else:
        selected_pet_name = st.selectbox("Select pet", [p.name for p in st.session_state.pets])
        selected_pet = next(p for p in st.session_state.pets if p.name == selected_pet_name)

        st.subheader(f"Add Task for {selected_pet_name}")
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("Task name", value="Morning Walk")
            task_type = st.selectbox("Type", ["exercise", "nutrition", "hygiene", "enrichment", "medication"])
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
            time_pref = st.selectbox("Time preference", ["morning", "afternoon", "evening", "none"])

        if st.button("Add Task", type="primary"):
            selected_pet.add_care_task(Task(
                name=task_name,
                type=task_type,
                priority=priority,
                duration=int(duration),
                frequency=frequency,
                time_preference=None if time_pref == "none" else time_pref
            ))
            st.success(f"'{task_name}' added to {selected_pet_name}!")
            st.rerun()

        # ── Task list ──
        all_tasks = selected_pet.get_all_tasks()
        if not all_tasks:
            st.info("No tasks yet — add one above.")
        else:
            st.divider()
            col_f, col_s = st.columns(2)
            with col_f:
                type_options = ["all"] + sorted({t.type for t in all_tasks})
                filter_type = st.selectbox("Filter by type", type_options, key="filter_type")
            with col_s:
                sort_by = st.selectbox("Sort by", ["priority", "duration", "name"], key="sort_tasks")

            filtered = [t for t in all_tasks if filter_type == "all" or t.type == filter_type]
            if sort_by == "priority":
                filtered = sorted(filtered, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))
            elif sort_by == "duration":
                filtered = sorted(filtered, key=lambda t: t.duration)
            elif sort_by == "name":
                filtered = sorted(filtered, key=lambda t: t.name)

            st.subheader(f"{selected_pet_name}'s Tasks ({len(filtered)} shown)")
            for t in filtered:
                col_info, col_del = st.columns([5, 1])
                with col_info:
                    pref = t.time_preference or "any time"
                    badge = PRIORITY_BADGE.get(t.priority, "")
                    st.markdown(f"{badge} **{t.name}** · _{t.type}_ · {t.duration} min · {pref} · _{t.frequency}_")
                with col_del:
                    if st.button("✕", key=f"del_task_{all_tasks.index(t)}_{selected_pet_name}", help="Remove task"):
                        selected_pet.remove_care_task(t)
                        st.rerun()


# ─────────────────────────────────────────────
# TAB 4: SCHEDULE
# ─────────────────────────────────────────────
with tab4:
    if st.session_state.owner is None:
        st.warning("Set up your owner profile first.")
    elif not st.session_state.pets:
        st.warning("Add pets and tasks before generating a schedule.")
    else:
        st.subheader("Generate Daily Schedules")

        col1, col2 = st.columns(2)
        with col1:
            day_start = st.text_input("Day start (HH:MM)", value="08:00")
        with col2:
            day_end = st.text_input("Day end (HH:MM)", value="22:00")

        pets_to_schedule = st.multiselect(
            "Pets to schedule",
            [p.name for p in st.session_state.pets],
            default=[p.name for p in st.session_state.pets]
        )

        if st.button("Generate Schedule", type="primary"):
            if not pets_to_schedule:
                st.warning("Select at least one pet.")
            else:
                generated = []
                for pname in pets_to_schedule:
                    pet = next(p for p in st.session_state.pets if p.name == pname)
                    if not pet.get_all_tasks():
                        st.warning(f"{pet.name} has no tasks — skipping.")
                        continue
                    scheduler = Scheduler(owner=st.session_state.owner, pet=pet, date=TODAY, day_start=day_start, day_end=day_end)
                    plan = scheduler.build_schedule()
                    st.session_state.plans[pname] = {
                        "plan": plan,
                        "scheduler": scheduler,
                        "explanation": scheduler.explain_plan(plan)
                    }
                    generated.append(pname)
                if generated:
                    st.success(f"Schedules generated for: {', '.join(generated)}")
                    st.rerun()

        # ── Display plans ─────────────────────────────
        if st.session_state.plans:
            st.divider()

            schedule_sort = st.radio("View by", ["time", "priority"], horizontal=True)

            # Conflict detection across all plans
            all_plans = [v["plan"] for v in st.session_state.plans.values()]
            if len(all_plans) > 1:
                any_scheduler = next(iter(st.session_state.plans.values()))["scheduler"]
                conflicts = any_scheduler.detect_conflicts(*all_plans)
                if conflicts:
                    with st.expander(f"⚠️ {len(conflicts)} conflict(s) detected across pets", expanded=True):
                        for w in conflicts:
                            st.warning(w)

            for pname, entry in st.session_state.plans.items():
                plan = entry["plan"]
                species_icon = {"dog": "🐕", "cat": "🐈"}.get(
                    next((p.species for p in st.session_state.pets if p.name == pname), "other"), "🐾"
                )
                st.markdown(f"### {species_icon} {pname}'s Schedule")

                if not plan.scheduled_tasks:
                    st.warning(f"No tasks could be scheduled for {pname} — check availability blocks.")
                    continue

                tasks_to_show = list(plan.scheduled_tasks)
                if schedule_sort == "priority":
                    tasks_to_show = sorted(tasks_to_show, key=lambda s: PRIORITY_ORDER.get(s.task.priority, 99))

                for i, sched_task in enumerate(tasks_to_show):
                    done = sched_task.is_complete
                    col_check, col_info = st.columns([1, 6])

                    with col_check:
                        checked = st.checkbox("", value=done, key=f"check_{pname}_{i}")
                        if checked and not sched_task.is_complete:
                            sched_task.mark_complete(on_date=TODAY)
                        elif not checked and sched_task.is_complete:
                            sched_task.task.mark_incomplete()
                            sched_task.is_complete = False
                            sched_task.next_task = None

                    with col_info:
                        badge = PRIORITY_BADGE.get(sched_task.task.priority, "")
                        line = (
                            f"{badge} **{sched_task.start_time}–{sched_task.end_time}** — "
                            f"{sched_task.task.name} ·  _{sched_task.task.priority} priority_ · "
                            f"{sched_task.task.duration} min"
                        )
                        if done:
                            st.markdown(
                                f"<span style='opacity:0.3;text-decoration:line-through;'>{line}</span>",
                                unsafe_allow_html=True
                            )
                            if sched_task.next_task:
                                st.caption(f"↻ Next due: {sched_task.next_task.due_date}")
                        else:
                            st.markdown(line)

                status = plan.get_completion_status()
                progress_val = status["complete"] / status["total"] if status["total"] > 0 else 0
                st.progress(progress_val)
                st.caption(f"{status['complete']}/{status['total']} complete · {status['remaining']} remaining")

                with st.expander("💡 Why this schedule?"):
                    st.text(entry["explanation"])

                st.divider()
