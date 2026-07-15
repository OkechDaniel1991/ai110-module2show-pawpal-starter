import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")
st.caption("Plan pet care tasks and keep them organized by owner and pet.")

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Mixed")
    pet_submitted = st.form_submit_button("Add pet")

if pet_submitted:
    new_pet = Pet(name=pet_name, species=species, breed=breed)
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} to {owner.name}'s pets.")

pets = owner.get_pets()

if pets:
    st.write("Current pets:")
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Breed": pet.breed}
            for pet in pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
if not pets:
    st.info("Add a pet before scheduling tasks.")
else:
    pet_options = {pet.name: pet for pet in pets}

    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox("Pet", list(pet_options.keys()))
        task_description = st.text_input("Task description", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly", "once"])
        scheduled_time = st.time_input("Scheduled time")
        task_submitted = st.form_submit_button("Schedule task")

    if task_submitted:
        selected_pet = pet_options[selected_pet_name]
        new_task = Task(
            description=task_description,
            duration_minutes=int(duration),
            frequency=frequency,
            scheduled_time=scheduled_time,
        )
        selected_pet.add_task(new_task)
        st.success(f"Scheduled {new_task.description} for {selected_pet.name}.")

scheduler = Scheduler(owner)
all_tasks = scheduler.sort_tasks_by_time()

if all_tasks:
    st.write("Scheduled tasks:")
    st.table(
        [
            {
                "Task": task.description,
                "Duration": task.duration_minutes,
                "Frequency": task.frequency,
                "Time": task.scheduled_time.strftime("%I:%M %p")
                if task.scheduled_time
                else "Unscheduled",
                "Complete": task.completed,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Schedule one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    pending_tasks = scheduler.get_pending_tasks()

    if not pending_tasks:
        st.info("No pending tasks to schedule.")
    else:
        st.write("Today's plan:")
        for task in scheduler.sort_tasks_by_time():
            if task.is_complete():
                continue

            time_label = (
                task.scheduled_time.strftime("%I:%M %p")
                if task.scheduled_time
                else "Unscheduled"
            )
            st.write(
                f"- {time_label}: {task.description} "
                f"({task.duration_minutes} min, {task.frequency})"
            )