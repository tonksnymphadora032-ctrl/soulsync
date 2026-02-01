import streamlit as st
import sqlite3
from datetime import date

conn = sqlite3.connect("soulsync.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry TEXT,
    mood TEXT,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")

conn.commit()


def save_journal(entry, mood):
    today = date.today().isoformat()

    if entry.strip() == "":
        st.warning("⚠️ Please write something first.")
        return

    cur.execute(
        "INSERT INTO journal (entry, mood, date) VALUES (?, ?, ?)",
        (entry, mood, today)
    )
    conn.commit()

    st.success("💙 Your thoughts are saved safely.")


def add_task(task):
    if task.strip() == "":
        return

    cur.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )
    conn.commit()


def get_tasks():
    cur.execute("SELECT task FROM tasks")
    return [t[0] for t in cur.fetchall()]


st.set_page_config(page_title="SoulSync", page_icon="🌱")

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



