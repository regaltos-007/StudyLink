import streamlit as st
from datetime import datetime
import uuid
def set_study_gradient():
    st.markdown("""
        <style>
           /* ---------------- Lo-Fi Aesthetic Animated Background ---------------- */
.stApp {
    background: linear-gradient(-45deg, #2a2550, #3b1c32, #1c1f4a, #4a2f60);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    color: #f2e9ff !important;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating particles like lofi dust */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: url("https://i.imgur.com/3ZQ3Z6F.png"); /* subtle dust texture */
    opacity: 0.28;
    pointer-events: none;
    animation: floatDust 12s linear infinite;
}

@keyframes floatDust {
    from { transform: translateY(0px); }
    to { transform: translateY(-40px); }
}

/* ---------------- Lo-Fi Text Area ---------------- */
textarea {
    background: rgba(255, 255, 255, 0.10) !important;
    border: 2px solid rgba(200, 150, 255, 0.45) !important;
    color: #fbe9ff !important;
    border-radius: 12px !important;
    backdrop-filter: blur(5px);
    padding: 14px !important;
    font-size: 17px !important;
    font-family: "Fira Code", monospace !important;
}

/* ---------------- Lo-Fi Button (Neon Glow) ---------------- */
.stButton > button {
    background: rgba(70, 40, 120, 0.6) !important;
    color: #f5e7ff !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    border: 1px solid #c39bff !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    text-shadow: 0 0 6px #b88fff;
    transition: 0.25s ease-in-out;
    backdrop-filter: blur(4px);
}

.stButton > button:hover {
    background: rgba(120, 70, 200, 0.8) !important;
    box-shadow: 0px 0px 12px #c39bff;
    transform: scale(1.05);
}

/* ---------------- Answer Box (Glassmorphic Lofi Card) ---------------- */
.stMarkdown, .stAlert {
    background: rgba(255, 255, 255, 0.12) !important;
    border-left: 4px solid #d8b3ff !important;
    border-radius: 14px !important;
    padding: 20px;
    color: #f8eaff !important;
    font-family: "Fira Code", monospace !important;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

/* ---------------- Sidebar (Dark Purple Glass) ---------------- */
.css-1d391kg, .css-1avcm0n {
    background: rgba(20, 10, 40, 0.65) !important;
    backdrop-filter: blur(6px) !important;
    color: #e8d5ff !important;
}

.css-1lcbmhc, .css-17lntkn {
    color: #e8d5ff !important;
}

/* Sidebar buttons */
.css-1q8dd3e, .css-1x8cf1d {
    background: rgba(100, 60, 180, 0.6) !important;
    color: white !important;
    border-radius: 8px !important;
}

/* ---------------- Headers ---------------- */
h1, h2, h3, h4 {
    font-family: "Fira Code", monospace !important;
    color: #ffeaff !important;
    text-shadow: 0px 0px 8px rgba(200, 150, 255, 0.6);
}


        </style>
    """, unsafe_allow_html=True)
set_study_gradient()



st.set_page_config(page_title="StudyLink", layout="wide")

# ---------------------------
# DATA STORAGE (In-Memory)
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin"}

if "doubts" not in st.session_state:
    st.session_state.doubts = []

if "notes" not in st.session_state:
    st.session_state.notes = []

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
def login_page():
    st.title("📘 StudyLink")
    st.subheader("Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
        else:
            st.error("Invalid login details")

    st.write("Don't have an account?")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    
    if st.button("Create Account"):
        if new_user in st.session_state.users:
            st.error("User already exists!")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created! Please login.")

# ---------------------------
# DOUBT SOLVING SECTION
# ---------------------------
def doubt_section():
    st.header("❓ Ask a Doubt")

    doubt_text = st.text_area("Write your question")
    
    if st.button("Submit Doubt"):
        if doubt_text.strip():
            st.session_state.doubts.append({
                "id": str(uuid.uuid4()),
                "user": st.session_state.username,
                "text": doubt_text,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Doubt posted successfully!")

    st.subheader("📚 Recent Doubts")

    for doubt in reversed(st.session_state.doubts):
        with st.expander(f"{doubt['text'][:50]}..."):
            st.write("Asked by:", doubt["user"])
            st.write("Time:", doubt["time"])
            answer = st.text_area(f"Write an answer for: {doubt['id']}")
            if st.button(f"Submit Answer {doubt['id']}"):
                st.success("Answer submitted (demo only).")

# ---------------------------
# NOTES SHARING SECTION
# ---------------------------
def notes_section():
    st.header("📄 Upload Notes")

    uploaded_file = st.file_uploader("Upload PDF, Image or Text notes")

    if uploaded_file:
        file_data = uploaded_file.read()
        st.session_state.notes.append({
            "filename": uploaded_file.name,
            "data": file_data,
            "user": st.session_state.username,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.success("Notes uploaded successfully!")

    st.subheader("📘 Shared Notes")

    for note in reversed(st.session_state.notes):
        with st.expander(f"{note['filename']} (Uploaded by {note['user']})"):
            st.write("Uploaded on:", note["time"])
            st.download_button("Download File", note["data"], file_name=note["filename"])

# ---------------------------
# AI DOUBT SOLVER (DEMO)
# ---------------------------
import streamlit as st
import requests

def ai_helper():
    st.header("🤖 AI Doubt Solver (Free With Groq AI)")

    user_q = st.text_area("Ask any study question")

    if st.button("Get Answer"):
        if not user_q.strip():
            st.warning("Enter a question first.")
            return

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": 
                 "You are StudyLink AI. Provide complete, detailed study answers with headings, bullet points, examples, and summaries."
                },
                {"role": "user", "content": user_q}
            ],
            "max_tokens": 1200,
            "temperature": 0.4,
            "top_p": 1
        }


        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                st.success(answer)

            else:
                st.error(f"API Error: {response.text}")

        except Exception as e:
            st.error(f"Error: {e}")



# ---------------------------
# MAIN APP UI
# ---------------------------
def main_app():
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    choice = st.sidebar.radio("Menu", ["Doubt Solving", "Upload Notes", "AI Helper"])

    if choice == "Doubt Solving":
        doubt_section()
    elif choice == "Upload Notes":
        notes_section()
    else:
        ai_helper()

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False

# ---------------------------
# RUN APP
# ---------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_page()
else:
    main_app()
