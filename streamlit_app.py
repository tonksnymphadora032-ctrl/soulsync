import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import date

st.set_page_config(page_title="SoulSync", page_icon="🌱")

# ---------- FIREBASE INIT ----------

db = None   # default

try:
    if not firebase_admin._apps:
        firebase_dict = json.loads(st.secrets["firebase_key"])

        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    st.success("✅ Firebase Connected")

except Exception as e:
    st.error("❌ Firebase Init Failed:")
    st.code(str(e))


# ---------- FUNCTIONS ----------

def save_journal(entry, mood):

    if db is None:
        st.error("Firebase not connected")
        return

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

    if db is None:
        st.error("Firebase not connected")
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
st.write("How are you feeling today?")

mood = st.selectbox(
    "Mood",
    ["Happy", "Okay", "Anxious", "Stressed",]()
