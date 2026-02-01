import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import tempfile
from datetime import date

st.set_page_config(page_title="SoulSync", page_icon="🌱")

db = None

# ---------- FIREBASE INIT ----------

try:
    if not firebase_admin._apps:

        # Write secret to temp file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            f.write(st.secrets["firebase_file"])
            key_path = f.name

        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    st.success("✅ Firebase Connected")

except Exception as e:
    st.error("❌ Firebase Error")
    st.code(str(e))


# ---------- FUNCTIONS ----------

def save_journal(entry, mood):

    if db is None:
        st.error("Firebase not connected")
        return

    if entry.strip() == "":
        return

    db.collection("journals").add({
        "entry": entry,
        "mood": mood,
        "date": str(date.today())
    })

    st.success("Saved!")


def add_task(task):

    if db is None:
        return

    if task.strip() == "":
        return

    db.collection("tasks").add({
        "task": task,
        "date": str(date.today())
    })


def get_tasks():

    if db is None:
        return []

    docs = db.collection("tasks").stream()
    return [d.to_dict()["task"] for d in docs]


# ---------- UI ----------

st.title("🌱 SoulSync")

mood = st.selectbox(
    "Mood",
    ["Happy", "Okay", "Anxious", "Stressed", "Low"]
)

st.subheader("📝 Journal")

entry = st.text_area("Write here")

if st.button("Save Journal"):
    save_journal(entry, mood)


st.subheader("✅ Tasks")

task = st.text_input("Enter task")

if st.button("Add Task"):
    add_task(task)
    st.experimental_rerun()


tasks = get_tasks()

if tasks:
    for t in tasks:
        st.write("•", t)

st.markdown("---")
st.markdown("_You are doing your best 💙_")
