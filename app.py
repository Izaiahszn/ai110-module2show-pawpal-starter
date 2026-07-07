import streamlit as st

# Step 1: bring the logic layer into the UI.
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# The UI uses friendly priority words; the logic layer uses ints (higher = more important).
PRIORITY_TO_INT = {"low": 1, "medium": 2, "high": 3}


# Step 2: keep one Owner alive across reruns.
# Streamlit re-runs this script top-to-bottom on every interaction, so we store the
# Owner in st.session_state (a dict-like "vault") and only create it once.
def get_owner() -> Owner:
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan", available_minutes=60)
    return st.session_state.owner


owner = get_owner()

# --- Owner settings -------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = st.number_input(
    "Available minutes today", min_value=1, max_value=1440, value=owner.available_minutes
)
owner.preferences = st.text_input("Preferences", value=owner.preferences)

st.divider()

# --- Add a pet ------------------------------------------------------------
# Step 3: submitting this form calls Owner.add_pet(), which persists in session_state.
st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet") and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name} the {species}.")

if not owner.pets:
    st.info("No pets yet. Add one above.")
    st.stop()

st.write("**Current pets:** " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))

st.divider()

# --- Add a task to a pet --------------------------------------------------
# Submitting this form calls Pet.add_task() on the chosen pet.
st.subheader("Add a task")
pet_names = [p.name for p in owner.pets]
with st.form("add_task", clear_on_submit=True):
    chosen_pet = st.selectbox("For which pet?", pet_names)
    task_title = st.text_input("Task title", value="Morning walk")
    category = st.text_input("Category", value="exercise")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    if st.form_submit_button("Add task") and task_title:
        pet = next(p for p in owner.pets if p.name == chosen_pet)
        pet.add_task(
            Task(
                name=task_title,
                category=category,
                duration=int(duration),
                priority=PRIORITY_TO_INT[priority],
            )
        )
        st.success(f"Added '{task_title}' to {chosen_pet}.")

# Show the tasks currently held on each pet.
all_tasks = owner.all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "task": t.name,
                "category": t.category,
                "duration (min)": t.duration,
                "priority": t.priority,
                "done": t.completed,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate the schedule ------------------------------------------------
# This button hands the Owner to the Scheduler and shows the plan + reasoning.
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.make_plan()
    if not plan:
        st.warning("No tasks fit in the available time. Add tasks or raise the time budget.")
    else:
        st.code(scheduler.display_plan(), language="text")
        st.markdown("**Why this plan?**")
        st.code(scheduler.explain(), language="text")
