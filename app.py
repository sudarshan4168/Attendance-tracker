import json
import os
from datetime import date
import streamlit as st

DATA_FILE = "attendance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "student_name": "Sudarshan Kumar",
            "working_days": 76,
            "present_days": 40,
            "history": []
        }
        save_data(default_data)
        return default_data
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Page Configuration
st.set_page_config(page_title="Attendance Tracker", page_icon="📈", layout="centered")

data = load_data()

# Calculate stats
total = data["working_days"]
present = data["present_days"]
absent = total - present
pct = (present / total * 100) if total > 0 else 0.0

st.title("📚 Attendance Tracker")
st.subheader(f"Student: {data['student_name']}")

# Visual Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Present Days", present)
col2.metric("Total Days", total)
col3.metric("Attendance %", f"{pct:.2f}%")

# Progress Bar
st.progress(min(pct / 100, 1.0))

# Warning / Success Banner
if pct < 75:
    needed = (3 * total) - (4 * present)
    st.error(f"⚠️ **Below 75%!** You need to attend the next **{needed}** consecutive classes to reach 75%.")
else:
    st.success("✅ **Good Job!** Your attendance is above the 75% target.")

st.divider()

# Daily Attendance Entry Form
st.header("📌 Mark Attendance")
with st.form("attendance_form", clear_on_submit=True):
    entry_date = st.date_input("Select Date", date.today())
    status = st.radio("Status", ["Present", "Absent"], horizontal=True)
    submitted = st.form_submit_button("Submit Attendance")

    if submitted:
        date_str = str(entry_date)
        
        # Check for duplicate entries
        if any(item["date"] == date_str for item in data["history"]):
            st.warning(f"Attendance for {date_str} is already logged!")
        else:
            data["working_days"] += 1
            if status == "Present":
                data["present_days"] += 1

            new_pct = (data["present_days"] / data["working_days"]) * 100
            
            data["history"].append({
                "date": date_str,
                "status": status,
                "percentage": round(new_pct, 2)
            })
            
            save_data(data)
            st.success(f"Logged **{status}** for {date_str}!")
            st.rerun()

# History Table
if data["history"]:
    st.divider()
    st.header("📜 Recent Logs")
    st.dataframe(data["history"], use_container_width=True)