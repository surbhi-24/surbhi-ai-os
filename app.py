import streamlit as st
import json
import random
from datetime import datetime
import ollama
import os

st.set_page_config(page_title="Surbhi AI OS", layout="wide")

st.title("🚀 Surbhi AI OS")

# -----------------------------
# Utility Functions
# -----------------------------

def load_data(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)

    with open(path) as f:
        return json.load(f)


def save_data(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# Load Databases
# -----------------------------
daily_log = load_data(
    "data/daily_log.json",
    {"academics": 0, "dsa": 0, "webdev": 0}
)

intern_tests = load_data(
    "data/intern_tests.json",
    {"tests": []}
)

dsa = load_data("data/dsa_questions.json", {"questions": []})

webdev_lectures = load_data(
    "data/webdev_lectures.json", {"lectures": []}
)

webdev_projects = load_data(
    "data/webdev_projects.json", {"projects": []}
)

academics = load_data(
    "data/academics.json", {"subjects": []}
)


# -----------------------------
# SIDEBAR – AI SCHEDULER
# -----------------------------

st.sidebar.header("📅 AI Study Scheduler")

exam_mode = st.sidebar.checkbox("Exam Season")
intern_mode = st.sidebar.checkbox("Internship / OA Soon")
holiday_mode = st.sidebar.checkbox("Long Holiday")

if exam_mode:

    st.sidebar.write("Suggested Schedule")

    st.sidebar.write("📚 Academics: 6 hr")
    st.sidebar.write("💻 DSA: 2 hr")
    st.sidebar.write("🌐 Web Dev: optional")

elif intern_mode:

    st.sidebar.write("Suggested Schedule")

    st.sidebar.write("💻 DSA: 5-6 hr")
    st.sidebar.write("📚 Academics: 1 hr minimum")
    st.sidebar.write("🌐 Web Dev: optional")

elif holiday_mode:

    st.sidebar.write("Suggested Schedule")

    st.sidebar.write("💻 DSA: 5 hr")
    st.sidebar.write("🌐 Web Dev: 3 hr")
    st.sidebar.write("📚 Academics: 1 hr revision")

else:

    st.sidebar.write("Regular Day Schedule")

    st.sidebar.write("📚 Academics: 3 hr")
    st.sidebar.write("💻 DSA: 3 hr")
    st.sidebar.write("🌐 Web Dev: 1 hr")


# -----------------------------
# DSA SECTION
# -----------------------------

st.header("💻 DSA Tracker")

topic = st.text_input("Topic")
problem = st.text_input("Problem Name")
platform = st.text_input("Platform")
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
notes = st.text_area("Notes")

if st.button("Save Problem"):

    new_problem = {
        "topic": topic,
        "problem": problem,
        "platform": platform,
        "difficulty": difficulty,
        "notes": notes,
        "date": str(datetime.today().date())
    }

    dsa["questions"].append(new_problem)

    save_data("data/dsa_questions.json", dsa)

    st.success("Problem saved!")


# -----------------------------
# DSA HISTORY
# -----------------------------

st.subheader("Solved Problems")

if len(dsa["questions"]) == 0:

    st.write("No problems solved yet.")

else:

    for q in dsa["questions"]:

        st.write(
            f"{q['date']} | {q['topic']} | {q['problem']} | {q['difficulty']} | {q['platform']}"
        )


# -----------------------------
# TOPIC PROGRESS
# -----------------------------

st.subheader("DSA Topic Progress")

topic_count = {}

for q in dsa["questions"]:

    topic = q["topic"]

    if topic not in topic_count:
        topic_count[topic] = 0

    topic_count[topic] += 1


if len(topic_count) == 0:

    st.write("No topic progress yet.")

else:

    for topic in topic_count:

        st.write(topic)

        progress = min(topic_count[topic] / 20, 1.0)

        st.progress(progress)


# -----------------------------
# WEB DEV LECTURES
# -----------------------------

st.header("🌐 Web Development Lectures")

lecture = st.text_input("Lecture Name")

if st.button("Add Lecture"):

    webdev_lectures["lectures"].append(
        {
            "lecture": lecture,
            "date": str(datetime.today().date())
        }
    )

    save_data("data/webdev_lectures.json", webdev_lectures)

    st.success("Lecture Added")


for lec in webdev_lectures["lectures"]:

    st.write(f"{lec['date']} | {lec['lecture']}")


# -----------------------------
# WEB DEV PROJECTS
# -----------------------------

st.header("🛠 Web Dev Projects")

project = st.text_input("Project Name")

if st.button("Add Project"):

    webdev_projects["projects"].append(
        {
            "project": project,
            "date": str(datetime.today().date())
        }
    )

    save_data("data/webdev_projects.json", webdev_projects)

    st.success("Project Added")


for p in webdev_projects["projects"]:

    st.write(f"{p['date']} | {p['project']}")


# -----------------------------
# ACADEMICS TRACKER
# -----------------------------

st.header("📚 Academics")

subject = st.text_input("Subject")

status = st.selectbox(
    "Status",
    ["Not Started", "In Progress", "Completed"]
)

if st.button("Add Subject"):

    academics["subjects"].append(
        {
            "subject": subject,
            "status": status
        }
    )

    save_data("data/academics.json", academics)

    st.success("Subject Added")


for s in academics["subjects"]:

    st.write(f"{s['subject']} — {s['status']}")
import json
from datetime import datetime

# Load exams
with open("data/exams.json") as f:
    exams = json.load(f)

today = datetime.today()

next_exam = None
next_exam_date = None
next_subject = None

for subject, exams_dict in exams["subjects"].items():
    for exam_name, date in exams_dict.items():

        if date is None:
            continue

        exam_date = datetime.strptime(date, "%Y-%m-%d")

        if exam_date >= today:

            if next_exam_date is None or exam_date < next_exam_date:
                next_exam_date = exam_date
                next_exam = exam_name
                next_subject = subject


if next_exam_date:
    days_left = (next_exam_date - today).days

    st.subheader("📅 Next Exam")

    st.write(f"Subject: {next_subject}")
    st.write(f"Exam: {next_exam}")
    st.write(f"Days Left: {days_left}")
st.subheader("📅 AI Study Scheduler")

if next_exam_date:

    if days_left <= 2:

        st.error("⚠️ Exam very close!")

        st.write("📚 Academics: 6 hr")
        st.write("💻 DSA: 1 hr")
        st.write("🌐 Web Dev: optional")

    elif days_left <= 7:

        st.warning("⚠️ Exam approaching")

        st.write("📚 Academics: 5 hr")
        st.write("💻 DSA: 2 hr")
        st.write("🌐 Web Dev: optional")

    else:

        st.success("✅ Regular Study Day")

        st.write("📚 Academics: 3 hr")
        st.write("💻 DSA: 3 hr")
        st.write("🌐 Web Dev: 1 hr")
st.header("🌙 Night Review")

st.write("Enter today's progress")

dsa_done = st.number_input("DSA problems solved today", 0, 20, 0)
lectures_done = st.number_input("Lectures completed", 0, 10, 0)
acad_hours = st.number_input("Academics hours studied", 0, 10, 0)

if st.button("Generate Review"):

    score = (dsa_done * 2) + lectures_done + acad_hours

    st.subheader("📊 Productivity Score")

    st.write(score)

    if score >= 10:
        st.success("🔥 Excellent day Surbhi")
    elif score >= 5:
        st.warning("⚠️ Decent day, can improve")
    else:
        st.error("❗ Low productivity day")

    st.subheader("📅 Tomorrow Plan")

    if next_exam_date and days_left <= 5:

        st.write("📚 Academics: 5 hr")
        st.write("💻 DSA: 2 hr")
        st.write("🌐 Web Dev: optional")
        st.write("🔁 Revision: 1 hr")

    else:

        st.write("📚 Academics: 3 hr")
        st.write("💻 DSA: 3 hr")
        st.write("🌐 Web Dev: 1 hr")
        st.write("🔁 Revision: 1 hr")
st.header("🤖 Surbhi AI Assistant")

user_prompt = st.text_area(
    "Ask AI (explain concept / generate quiz / study advice)"
)

if st.button("Ask AI"):

    if user_prompt:

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant helping Surbhi plan studies, explain concepts, generate quizzes and give study advice."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        answer = response["message"]["content"]

        st.subheader("AI Response")

        st.write(answer)
with open("data/exams.json") as f:
    exams = json.load(f)
def days_until(date_str):

    if date_str is None:
        return None

    exam_date = datetime.strptime(date_str, "%Y-%m-%d")
    today = datetime.today()

    return (exam_date - today).days
def nearest_exam():

    min_days = 999

    for subject in exams["subjects"]:

        for exam in exams["subjects"][subject]:

            date = exams["subjects"][subject][exam]

            d = days_until(date)

            if d is not None and d >= 0 and d < min_days:
                min_days = d

    return min_days
def generate_plan():

    exam_days = nearest_exam()

    academics = 3
    dsa = 3
    webdev = 1

    if exam_days is not None:

        if exam_days < 7:
            academics = 5
            dsa = 1
            webdev = 0

        elif exam_days < 14:
            academics = 4
            dsa = 2
            webdev = 1

    return academics, dsa, webdev
st.header("📅 AI Study Scheduler")

academics, dsa, webdev = generate_plan()

st.write("📚 Academics:", academics, "hr")
st.write("💻 DSA:", dsa, "hr")

if webdev > 0:
    st.write("🌐 Web Dev:", webdev, "hr")

st.write("🔁 Revision: 1 hr")
def nearest_intern_test():

    min_days = 999

    for test in intern_tests["tests"]:

        date = test.get("date")

        d = days_until(date)

        if d is not None and d >= 0 and d < min_days:
            min_days = d

    return min_days
def generate_plan():

    exam_days = nearest_exam()
    intern_days = nearest_intern_test()

    academics = 3
    dsa = 3
    webdev = 1

    # Internship priority
    if intern_days is not None and intern_days < 7:

        academics = 1
        dsa = 5
        webdev = 0

        return academics, dsa, webdev

    # Exam priority
    if exam_days is not None:

        if exam_days < 6:
            academics = 5
            dsa = 1
            webdev = 0

        elif exam_days < 10:
            academics = 4
            dsa = 2
            webdev = 1

    return academics, dsa, webdev
st.header("🌙 Night Review")

acad_done = st.number_input("Academics hours today", 0.0, 12.0, 0.0)
dsa_done = st.number_input("DSA hours today", 0.0, 12.0, 0.0)
web_done = st.number_input("Web Dev hours today", 0.0, 12.0, 0.0)
if st.button("Analyze Day"):

    academics, dsa, webdev = generate_plan()

    score = 0

    if acad_done >= academics:
        score += 4
    elif acad_done >= academics * 0.7:
        score += 3
    else:
        score += 1

    if dsa_done >= dsa:
        score += 4
    elif dsa_done >= dsa * 0.7:
        score += 3
    else:
        score += 1

    if web_done >= webdev:
        score += 2

    st.subheader("Performance Score")

    st.write("Score:", score, "/10")

    if score >= 8:
        st.success("Great day. Maintain consistency.")
    elif score >= 6:
        st.warning("Good effort. Slight improvement needed.")
    else:
        st.error("Low productivity. Prioritize academics tomorrow.")
st.header("🚀 AI Task Generator")

dsa_tasks = [
    "4 problems"
]

acad_tasks = [
    "DBMS revision",
    "DAA notes",
    "FLAT revision",
    "CAO revision",
    "SOCIO revision"
]

web_tasks = [
    "1 hr lec"
]

import random

if st.button("Generate Today's Tasks"):

    academics, dsa, webdev = generate_plan()

    st.subheader("Today's Tasks")

    st.write("📚 Academics")

selected_subjects = st.multiselect(
    "Select subjects to study today",
    acad_tasks
)

for subject in selected_subjects:
    st.write("•", subject)

    st.write("💻 DSA")

    for task in dsa_tasks:
        st.write("•", task)

    st.write("🌐 Web Dev")

    for task in web_tasks:
        st.write("•", task)
