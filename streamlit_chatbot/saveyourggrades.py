
import streamlit as st
import pandas as pd
import random
from datetime import datetime, date, time, timedelta

# =====================================================
# Student Time Management App
# Features:
# 1. Editable task checklist with add-new-task button
# 2. Past reminders section
# 3. Productivity tip changes each time the app refreshes
# 4. Editable timetable with date/time and flexible columns
# 5. Interactive Pomodoro timer with subject choice
# =====================================================

st.set_page_config(
    page_title="Student Time Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS: ChatGPT-like clean layout
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7f7f8 0%, #ffffff 100%);
    }
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #202123;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.07);
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
    }
    .metric-card {
        background-color: white;
        border-radius: 16px;
        padding: 18px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }
    .tip-box {
        background-color: #f0fdf4;
        color: #166534;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #bbf7d0;
        font-size: 16px;
    }
    .past-box {
        background-color: #fff7ed;
        color: #9a3412;
        padding: 14px;
        border-radius: 14px;
        border: 1px solid #fed7aa;
    }
    .timer-display {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        color: #111827;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session state setup
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame({
        "Done": [False, False],
        "Task": ["Revise lecture notes", "Submit assignment"],
        "Subject": ["Mathematics", "English"],
        "Due Date": [date.today(), date.today() + timedelta(days=2)],
        "Due Time": [time(18, 0), time(23, 59)],
        "Priority": ["Medium", "High"],
        "Reminder Note": ["Review examples", "Upload to Moodle"]
    })

if "timetable" not in st.session_state:
    st.session_state.timetable = pd.DataFrame({
        "Date": [date.today(), date.today() + timedelta(days=1)],
        "Start Time": [time(9, 0), time(11, 0)],
        "End Time": [time(10, 30), time(12, 30)],
        "Subject/Class": ["Mathematics", "Study Group"],
        "Location": ["Room A", "Library"],
        "Notes": ["Bring calculator", "Group discussion"]
    })

if "pomodoro_seconds" not in st.session_state:
    st.session_state.pomodoro_seconds = 25 * 60

if "pomodoro_running" not in st.session_state:
    st.session_state.pomodoro_running = False

if "pomodoro_subject" not in st.session_state:
    st.session_state.pomodoro_subject = "General Study"

if "pomodoro_log" not in st.session_state:
    st.session_state.pomodoro_log = []

if "custom_columns" not in st.session_state:
    st.session_state.custom_columns = []

# -----------------------------
# Helper functions
# -----------------------------
def add_task():
    new_row = pd.DataFrame({
        "Done": [False],
        "Task": ["New task"],
        "Subject": ["General"],
        "Due Date": [date.today()],
        "Due Time": [time(12, 0)],
        "Priority": ["Medium"],
        "Reminder Note": [""]
    })
    st.session_state.tasks = pd.concat([st.session_state.tasks, new_row], ignore_index=True)


def clear_completed_tasks():
    st.session_state.tasks = st.session_state.tasks[st.session_state.tasks["Done"] == False].reset_index(drop=True)


def add_timetable_row():
    new_row = pd.DataFrame({
        "Date": [date.today()],
        "Start Time": [time(9, 0)],
        "End Time": [time(10, 0)],
        "Subject/Class": ["New class"],
        "Location": [""],
        "Notes": [""]
    })

    for col in st.session_state.custom_columns:
        new_row[col] = ""

    st.session_state.timetable = pd.concat([st.session_state.timetable, new_row], ignore_index=True)


def add_custom_column(column_name):
    if column_name and column_name not in st.session_state.timetable.columns:
        st.session_state.timetable[column_name] = ""
        st.session_state.custom_columns.append(column_name)


def get_due_datetime(row):
    try:
        return datetime.combine(row["Due Date"], row["Due Time"])
    except Exception:
        return None


def start_pomodoro(minutes, subject):
    st.session_state.pomodoro_seconds = int(minutes) * 60
    st.session_state.pomodoro_subject = subject
    st.session_state.pomodoro_running = True


def reset_pomodoro(minutes):
    st.session_state.pomodoro_seconds = int(minutes) * 60
    st.session_state.pomodoro_running = False

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">📚 Student Time Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Plan your classes, tasks, reminders, and focused study sessions in one place.</div>', unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    ["Dashboard", "Tasks & Reminders", "Editable Timetable", "Pomodoro Timer", "Study Log"]
)

productivity_tips = [
    "Use the 2-minute rule: if a task takes less than 2 minutes, do it now.",
    "Study one subject at a time to reduce mental switching.",
    "Start with the hardest task first when your energy is highest.",
    "Break big assignments into small checklist items.",
    "Review your timetable every morning before class.",
    "Use Pomodoro sessions for focused study and short breaks.",
    "Keep your phone away during deep study blocks.",
    "Write tomorrow’s top 3 tasks before sleeping.",
    "Use deadlines as planning tools, not panic tools.",
    "After every class, spend 10 minutes summarising key points."
]

# Tip updates on every reload/rerun
current_tip = random.choice(productivity_tips)

# -----------------------------
# Dashboard
# -----------------------------
if page == "Dashboard":
    st.markdown("### Welcome back 👋")

    total_tasks = len(st.session_state.tasks)
    completed_tasks = int(st.session_state.tasks["Done"].sum()) if total_tasks > 0 else 0
    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{total_tasks}</h3><p>Total Tasks</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{pending_tasks}</h3><p>Pending Tasks</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{completed_tasks}</h3><p>Completed Tasks</p></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### 🌱 Productivity Tip")
    st.markdown(f'<div class="tip-box">{current_tip}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### 🔔 Upcoming Reminders")
    now = datetime.now()

    reminders = st.session_state.tasks.copy()
    reminders["Due Datetime"] = reminders.apply(get_due_datetime, axis=1)
    upcoming = reminders[(reminders["Done"] == False) & (reminders["Due Datetime"] >= now)].sort_values("Due Datetime")

    if len(upcoming) == 0:
        st.info("No upcoming reminders. Add a new task to begin.")
    else:
        st.dataframe(upcoming[["Task", "Subject", "Due Date", "Due Time", "Priority", "Reminder Note"]], use_container_width=True)

    st.markdown("### ⏰ Today’s Classes")
    today_classes = st.session_state.timetable[st.session_state.timetable["Date"] == date.today()]
    if len(today_classes) == 0:
        st.info("No classes scheduled for today.")
    else:
        st.dataframe(today_classes, use_container_width=True)

# -----------------------------
# Tasks & Reminders
# -----------------------------
elif page == "Tasks & Reminders":
    st.markdown("### ✅ Checklist and Reminders")

    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        st.button("➕ Add New Task", on_click=add_task, use_container_width=True)
    with button_col2:
        st.button("🧹 Clear Completed Tasks", on_click=clear_completed_tasks, use_container_width=True)

    edited_tasks = st.data_editor(
        st.session_state.tasks,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Done": st.column_config.CheckboxColumn("Done"),
            "Task": st.column_config.TextColumn("Task", required=True),
            "Subject": st.column_config.TextColumn("Subject"),
            "Due Date": st.column_config.DateColumn("Due Date"),
            "Due Time": st.column_config.TimeColumn("Due Time"),
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=["Low", "Medium", "High"]
            ),
            "Reminder Note": st.column_config.TextColumn("Reminder Note")
        },
        key="task_editor"
    )
    st.session_state.tasks = edited_tasks

    st.markdown("### 📌 Past Reminders")
    now = datetime.now()
    past = st.session_state.tasks.copy()
    past["Due Datetime"] = past.apply(get_due_datetime, axis=1)
    past_reminders = past[(past["Done"] == False) & (past["Due Datetime"] < now)].sort_values("Due Datetime")

    if len(past_reminders) == 0:
        st.success("No overdue reminders. Great job!")
    else:
        st.markdown('<div class="past-box">These reminders are past their due date/time.</div>', unsafe_allow_html=True)
        st.dataframe(past_reminders[["Task", "Subject", "Due Date", "Due Time", "Priority", "Reminder Note"]], use_container_width=True)

# -----------------------------
# Editable Timetable
# -----------------------------
elif page == "Editable Timetable":
    st.markdown("### 🗓️ Editable Class Timetable")
    st.write("You can edit the timetable directly, add rows, add date/time, and create your own extra columns.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.button("➕ Add Timetable Row", on_click=add_timetable_row, use_container_width=True)
    with col2:
        new_column = st.text_input("Add a new column, e.g. Lecturer, Room Type, Homework")
        if st.button("Add Column", use_container_width=True):
            add_custom_column(new_column)
            st.rerun()

    column_config = {
        "Date": st.column_config.DateColumn("Date"),
        "Start Time": st.column_config.TimeColumn("Start Time"),
        "End Time": st.column_config.TimeColumn("End Time"),
        "Subject/Class": st.column_config.TextColumn("Subject/Class"),
        "Location": st.column_config.TextColumn("Location"),
        "Notes": st.column_config.TextColumn("Notes")
    }

    edited_timetable = st.data_editor(
        st.session_state.timetable,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        key="timetable_editor"
    )
    