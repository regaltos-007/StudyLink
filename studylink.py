import streamlit as st
from datetime import datetime
import uuid
def set_study_gradient():
    st.markdown("""
    <style>

    /* ===========================================
       1) STUDY DESK NIGHT BACKGROUND
       =========================================== */
    .stApp {
        background: linear-gradient(180deg, #120c1f 0%, #1a142b 35%, #2a1c15 80%);
        background-attachment: fixed;
        color: #f5e6d3 !important;
        position: relative;
        overflow: hidden;
        font-family: 'Georgia', serif;
    }

    /* Dark top → warm desk bottom */
    
    /* ===========================================
       2) DESK SURFACE (wood-like texture with CSS)
       =========================================== */
    .stApp::after {
        content: "";
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 35vh; /* desk height */
        background: 
            repeating-linear-gradient(
                90deg,
                rgba(120, 70, 40, 0.25) 0px,
                rgba(120, 70, 40, 0.25) 3px,
                rgba(150, 100, 60, 0.25) 3px,
                rgba(150, 100, 60, 0.25) 6px
            ),
            linear-gradient(180deg, #3e2717, #2d1a10);
        filter: brightness(1.3);
        z-index: -1;
    }

    /* ===========================================
       3) LAMP GLOW EFFECT
       =========================================== */
    .lampGlow {
        position: fixed;
        top: 18%;
        right: 22%;
        width: 300px;
        height: 300px;
        background: radial-gradient(
            circle,
            rgba(255, 230, 150, 0.55) 0%,
            rgba(255, 200, 120, 0.25) 35%,
            rgba(255, 180, 90, 0.12) 55%,
            rgba(255, 160, 70, 0.05) 70%,
            transparent 90%
        );
        border-radius: 50%;
        animation: glowPulse 4s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes glowPulse {
        0% { opacity: 0.45; transform: scale(1); }
        100% { opacity: 0.65; transform: scale(1.13); }
    }

    /* ===========================================
       4) VIGNETTE FOR DEPTH
       =========================================== */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background: radial-gradient(
            circle at center,
            transparent 40%,
            rgba(0, 0, 0, 0.4) 100%
        );
        pointer-events: none;
        z-index: -2;
    }

    /* ===========================================
       5) TEXTAREA - warm lamp highlight
       =========================================== */
    textarea {
        background: rgba(255, 245, 225, 0.12) !important;
        backdrop-filter: blur(6px);
        border-radius: 12px !important;
        border: 1px solid rgba(255, 212, 150, 0.35) !important;
        padding: 14px !important;
        font-size: 17px !important;
        color: #ffeccc !important;
    }

    /* ===========================================
       6) BUTTON - warm lamp button style
       =========================================== */
    .stButton > button {
        background: rgba(255, 200, 140, 0.18) !important;
        border: 1px solid rgba(255, 180, 120, 0.45) !important;
        border-radius: 10px !important;
        padding: 9px 18px !important;
        color: #ffe5c7 !important;
        font-size: 16px !important;
        transition: 0.25s;
        text-shadow: 0 0 8px rgba(255, 200, 150, 0.5);
    }

    .stButton > button:hover {
        background: rgba(255, 190, 110, 0.35) !important;
        box-shadow: 0 0 18px rgba(255, 210, 160, 0.6);
        transform: scale(1.05);
    }

    /* ===========================================
       7) ANSWER BOX (glass warm panel)
       =========================================== */
    .stAlert, .stMarkdown {
        background: rgba(255, 240, 220, 0.08) !important;
        border-left: 4px solid rgba(255, 200, 140, 0.7) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        color: #ffe7c9 !important;
        backdrop-filter: blur(6px);
    }

    /* ===========================================
       8) SIDEBAR
       =========================================== */
    .css-1d391kg, .css-1avcm0n {
        background: rgba(20, 12, 6, 0.55) !important;
        color: #ffe4c7 !important;
        backdrop-filter: blur(4px);
    }

    h1, h2, h3 {
        color: #ffe8c9 !important;
        text-shadow: 0 0 8px rgba(255, 220, 160, 0.4);
    }

    </style>

    <div class="lampGlow"></div>
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
