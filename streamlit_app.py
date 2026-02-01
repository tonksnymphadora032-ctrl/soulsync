import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import date

st.set_page_config(page_title="SoulSync", page_icon="🌱")

# ---------- FIREBASE INIT ----------

if not firebase_admin._apps:
    try:
        firebase_dict = json.loads(st.secrets["firebase_key"])
        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)
        st.success("✅ Firebase Connected")
    except Exception as e:
        st.error("❌ Firebase Error: " + str(e))

db = firestore.client()

# ---------- FUNCTIONS ----------

def save_journal(entry, mood):
    if entry.strip() == "":
        st.warning("⚠️ Please write something first.")
        return

    db.collection("journals").add({
        "entry": entry,
        "mood": mood,
        "date": str(date.today())
    })

    st.success("💙 Journal saved!")


def add_task(task):
    if task.strip() == "":
        return

    db.collection("tasks").add({
        "task": task,
        "date": str(date.today())
    })


def get_tasks():
    docs = db.collection("tasks").stream()
    return [d.to_dict()["task"] for d in docs]

# ---------- UI ----------

st.title("🌱 SoulSync")
st.write("How are you feeling today?")

mood = st.selectbox(
    "Mood",
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
    st.write("Your Tasks:")
    for t in tasks:
        st.write("•", t)

st.markdown("---")
st.markdown("_You are doing your best 💙_")
