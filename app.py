import streamlit as st
import pandas as pd
import json
import os

# Page setup
st.set_page_config(
    page_title="PM SHRI KV Muzaffarpur | Class 12-A", 
    page_icon="🏫", 
    layout="wide"
)

# --- CUSTOM CSS & ANIMATION STYLES ---
st.markdown("""
    <style>
    /* Global font & background adjustments */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Keyframe Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
        50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.6); }
        100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
    }

    /* Main Container Animation */
    .block-container {
        animation: fadeIn 0.8s ease-in-out;
    }

    /* Gradient Header */
    .main-title {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 25px;
        font-weight: 600;
    }

    /* Animated Stat Metric Cards */
    .metric-card {
        background: #1E1E2E;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-in-out;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        animation: pulseGlow 2s infinite;
        border-color: #6366F1;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #F3F4F6;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Main Banner Title
st.markdown('<h1 class="main-title">🏫 PM SHRI KV MUZAFFARPUR</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Class 12-A • Interactive Attendance Portal</p>', unsafe_allow_html=True)

DATA_FILE = "student_data.json"

DEFAULT_STUDENTS = {
    "1001194429": {"name": "RITU RAJ", "working": 76, "present": 19, "absent": 57},
    "1001195210": {"name": "PRIYANSHU KUMAR", "working": 76, "present": 26, "absent": 50},
    "1001195261": {"name": "RAHUL KUMAR", "working": 76, "present": 29, "absent": 47},
    "1001195212": {"name": "MD AJMAL", "working": 76, "present": 30, "absent": 46},
    "1001195251": {"name": "MD MOZAMMIL", "working": 76, "present": 34, "absent": 42},
    "1000986303": {"name": "SUDARSHAN KUMAR", "working": 76, "present": 40, "absent": 36},
    "1001194536": {"name": "ADIBA FAIYAZ", "working": 76, "present": 42, "absent": 34},
    "1001195256": {"name": "DHANANJAY GUPTA", "working": 76, "present": 42, "absent": 34},
    "1001195249": {"name": "NIHAL KUMAR SINGH", "working": 76, "present": 44, "absent": 32},
    "1001195260": {"name": "TEJASWI RAJ", "working": 76, "present": 44, "absent": 32},
    "1001196511": {"name": "SHRISTY KUMARI", "working": 76, "present": 45, "absent": 31},
    "1001194532": {"name": "SANKET KUMAR SINGH", "working": 76, "present": 46, "absent": 30},
    "1001196496": {"name": "HARSHIT ANAND", "working": 76, "present": 48, "absent": 28},
    "1001194530": {"name": "SHAFA PRAVEEN", "working": 76, "present": 48, "absent": 28},
    "1001195258": {"name": "TEJAS", "working": 76, "present": 48, "absent": 28},
    "1001194485": {"name": "VARSHA", "working": 76, "present": 48, "absent": 28},
    "1001196494": {"name": "SOMA RAJ", "working": 76, "present": 49, "absent": 27},
    "1001194451": {"name": "KRITIKA", "working": 76, "present": 50, "absent": 26},
    "1001197897": {"name": "ADARSH RAUNIYAR", "working": 76, "present": 51, "absent": 25},
    "1001196510": {"name": "AMAN KUMAR", "working": 76, "present": 53, "absent": 23},
    "1001196516": {"name": "MAHI KUMARI", "working": 76, "present": 53, "absent": 23},
    "1001195267": {"name": "NITYANSHU", "working": 76, "present": 54, "absent": 22},
    "1001194458": {"name": "AFZAL RAHMAN", "working": 76, "present": 55, "absent": 21},
    "1001194533": {"name": "ABHIGYAN DUBEY", "working": 76, "present": 56, "absent": 20},
    "1001196462": {"name": "GYANVI", "working": 76, "present": 56, "absent": 20}
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_STUDENTS

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

students = load_data()

# --- Sidebar ---
st.sidebar.markdown("### 🔍 Select Student")
student_options = {f"{info['name']} ({sid})": sid for sid, info in students.items()}
selected_label = st.sidebar.selectbox("Choose student name:", list(student_options.keys()))
selected_id = student_options[selected_label]
student_info = students[selected_id]

# --- Attendance Entry ---
st.markdown(f"### 📝 Mark Daily Attendance for **{student_info['name']}**")

col1, col2 = st.columns(2)
with col1:
    mark_date = st.date_input("Date")
with col2:
    status = st.radio("Status:", ["Present", "Absent"], horizontal=True)

if st.button("✨ Submit Attendance"):
    student_info["working"] += 1
    if status == "Present":
        student_info["present"] += 1
    else:
        student_info["absent"] += 1
    
    students[selected_id] = student_info
    save_data(students)
    st.balloons()
    st.success(f"Recorded {status} for {student_info['name']}!")
    st.rerun()

st.divider()

# --- Animated Metric Display Cards ---
pct = (student_info["present"] / student_info["working"]) * 100 if student_info["working"] > 0 else 0

st.markdown(f"### 📊 Live Performance Stats")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{student_info['working']}</div>
            <div class="metric-label">Working Days</div>
        </div>
    ''', unsafe_allow_html=True)

with c2:
    st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value" style="color: #10B981;">{student_info['present']}</div>
            <div class="metric-label">Present Days</div>
        </div>
    ''', unsafe_allow_html=True)

with c3:
    st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value" style="color: #EF4444;">{student_info['absent']}</div>
            <div class="metric-label">Absent Days</div>
        </div>
    ''', unsafe_allow_html=True)

with c4:
    color = "#10B981" if pct >= 75 else ("#F59E0B" if pct >= 60 else "#EF4444")
    st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value" style="color: {color};">{pct:.1f}%</div>
            <div class="metric-label">Attendance %</div>
        </div>
    ''', unsafe_allow_html=True)

st.write("")
st.divider()

# --- Class Roster Table ---
st.markdown("### 📋 Class 12-A Master Roster")

table_data = []
for sid, info in students.items():
    working = info["working"]
    present = info["present"]
    absent = info["absent"]
    percentage = round((present / working) * 100, 2) if working > 0 else 0
    
    table_data.append({
        "Student ID": sid,
        "Name": info["name"],
        "Working Days": working,
        "Present": present,
        "Absent": absent,
        "Attendance %": f"{percentage}%"
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)
