import streamlit as st
import pandas as pd
import json
import os

# Page configuration
st.set_page_config(page_title="Multi-Student Attendance Tracker", layout="centered")

st.title("📚 Student Attendance Tracker")

# Local file storage for attendance data
DATA_FILE = "attendance_data.json"

# Load existing data or initialize
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"Sudarshan": {}, "Harishat Anand": {}}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

attendance_data = load_data()

# --- Student Selection & Addition ---
st.sidebar.header("Student Management")
student_list = list(attendance_data.keys())
selected_student = st.sidebar.selectbox("Select Student:", student_list)

new_student = st.sidebar.text_input("Add New Student:")
if st.sidebar.button("Add Student"):
    if new_student and new_student not in attendance_data:
        attendance_data[new_student] = {}
        save_data(attendance_data)
        st.sidebar.success(f"Added {new_student}!")
        st.rerun()

st.header(f"Record for: **{selected_student}**")

# --- Date & Status Entry ---
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Select Date")
with col2:
    status = st.radio("Mark Status:", ["Present", "Absent"])

date_str = str(selected_date)

if st.button("Save Attendance"):
    attendance_data[selected_student][date_str] = status
    save_data(attendance_data)
    st.success(f"Marked {status} for {selected_student} on {date_str}!")
    st.rerun()

# --- Attendance Summary & Calculation ---
st.divider()
st.subheader("📊 Attendance Summary")

student_records = attendance_data.get(selected_student, {})

# Calculate ONLY logged days
total_logged_days = len(student_records)
present_count = sum(1 for s in student_records.values() if s == "Present")
absent_count = sum(1 for s in student_records.values() if s == "Absent")

if total_logged_days > 0:
    percentage = (present_count / total_logged_days) * 100
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Logged Days", total_logged_days)
    m2.metric("Present", present_count)
    m3.metric("Absent", absent_count)
    m4.metric("Attendance %", f"{percentage:.1f}%")

    # Display History Table
    st.subheader("📜 Detailed History")
    df = pd.DataFrame(list(student_records.items()), columns=["Date", "Status"])
    df = df.sort_values(by="Date", ascending=False)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No attendance recorded yet for this student. Mark a day above to start tracking!")
