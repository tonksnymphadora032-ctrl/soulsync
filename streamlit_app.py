import streamlit as st
from supabase import create_client
from datetime import date

# ---------------- CONFIG ----------------

st.set_page_config(page_title="SoulSync", page_icon="🌱")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- FUNCTIONS ----------------

def save_journal(entry, mood):

    if entry.strip() == "":
        st.warning("Write something first")
        return

    supabase.table("journals").insert({
        "entry": entry,
        "mood": mood,
        "date": str(date.today())
    }).execute()

    st.success("Saved!")


def add_task(task):

    if task.strip() == "":
        return

    supabase.table("tasks").insert({
        "task": task,
        "date": str(date.today())
    }).execute()


def get_tasks():

    data = supabase.table("tasks").select("task").execute()

    if data.data:
        return [x["task"] for x in data.data]

    return []


# ---------------- UI ----------------

st.title("🌱 SoulSync 🌱")

mood = st.selectbox(
    "How are you feeling today?",
    ["Happy", "Okay", "Anxious", "Stressed", "Low"]
)

st.subheader("📝 Journal")

entry = st.text_area("Write here...")

if st.button("Save Journal"):
    save_journal(entry, mood)


st.subheader("✅ Today's Tasks")

task = st.text_input("Enter task")

if st.button("Add Task"):
    add_task(task)
    st.experimental_rerun()


tasks = get_tasks()

if tasks:
    for t in tasks:
        st.write("•", t)


st.markdown("---")
st.markdown("💙 You are doing your best")
