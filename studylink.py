import streamlit as st
from datetime import datetime
import uuid
def set_study_gradient():
    st.markdown("""
    <style>

    /* --------------------------------------------------
       MAIN LOFI ANIMATED BACKGROUND (NO IMAGE NEEDED)
    --------------------------------------------------*/
    .stApp {
        background: linear-gradient(-45deg, #2b1e45, #3d255a, #1d2348, #4a2f60);
        background-size: 400% 400%;
        animation: gradientFlow 20s ease infinite;
        color: #f3eaff !important;
        position: relative;
        overflow: hidden;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --------------------------------------------------
        FLOATING PARTICLE / LOFI DUST EFFECT
        (generated with CSS, no external image!)
    --------------------------------------------------*/
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 1px, transparent 2px);
        background-size: 4px 4px;
        opacity: 0.14;
        animation: dustFloat 12s linear infinite;
    }

    @keyframes dustFloat {
        from { transform: translateY(0px); }
        to { transform: translateY(-40px); }
    }

    /* --------------------------------------------------
       TEXTAREA (LoFi glass style)
    --------------------------------------------------*/
    textarea {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(6px);
        border-radius: 12px !important;
        padding: 14px !important;
        border: 1px solid rgba(220, 180, 255, 0.4) !important;
        font-size: 17px !important;
        color: #f7e9ff !important;
        font-family: "Fira Code", monospace !important;
    }

    /* --------------------------------------------------
        BUTTON (LoFi neon glow)
    --------------------------------------------------*/
    .stButton > button {
        background: rgba(100, 60, 180, 0.65) !important;
        border: 1px solid #d8b3ff !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        text-shadow: 0 0 6px #caaaff;
        transition: 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background: rgba(150, 90, 230, 0.85) !important;
        box-shadow: 0 0 12px #e6c9ff;
        transform: scale(1.05);
    }

    /* --------------------------------------------------
        GLASS CARD FOR AI ANSWER
    --------------------------------------------------*/
    .stAlert, .stMarkdown {
        background: rgba(255,255,255,0.10) !important;
        backdrop-filter: blur(8px);
        padding: 20px !important;
        border-radius: 12px !important;
        border-left: 4px solid #e2baff !important;
        color: #f7e9ff !important;
        font-family: "Fira Code", monospace !important;
    }

    /* --------------------------------------------------
        SIDEBAR
    --------------------------------------------------*/
    .css-1d391kg, .css-1avcm0n {
        background: rgba(20, 10, 40, 0.55) !important;
        backdrop-filter: blur(6px);
        color: #e8d5ff !important;
    }

    h1, h2, h3 {
        color: #ffeaff !important;
        text-shadow: 0 0 10px rgba(230,200,255,0.5);
        font-family: "Fira Code", monospace !important;
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
