import streamlit as st
from datetime import datetime
import uuid
def set_study_gradient():
    st.markdown("""
        <style>
            /* ----- Page Background: Soft Library with Wooden Desk Overlay ----- */
.stApp {
    background: 
        linear-gradient(rgba(20, 15, 10, 0.55), rgba(20, 15, 10, 0.70)),
        url('https://images.unsplash.com/photo-1515165562835-c4c7e73e8fcf');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #f3e8d0 !important;
}

/* ----- Text Area (Notebook-style input) ----- */
textarea {
    background-color: rgba(255, 248, 225, 0.85) !important;
    color: #3b2f2f !important;
    border-radius: 10px !important;
    border: 2px solid #d3b98c !important;
    font-family: "Georgia", serif !important;
    font-size: 17px !important;
}

/* ----- Buttons (Wooden feel) ----- */
.stButton > button {
    background-color: #8b5e3b !important;
    color: #fff8e6 !important;
    border-radius: 8px !important;
    border: 2px solid #6d4c32 !important;
    padding: 8px 20px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: "Georgia", serif !important;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background-color: #a9744e !important;
    border-color: #8b5e3b !important;
    transform: scale(1.05);
}

/* ----- Answer Box (Paper card on wooden desk) ----- */
.stMarkdown, .stAlert {
    background: rgba(255, 248, 230, 0.92) !important;
    border-left: 6px solid #8b5e3b !important;
    padding: 18px;
    border-radius: 10px;
    color: #3b2f2f !important;
    font-family: "Georgia", serif !important;
    line-height: 1.6 !important;
    font-size: 18px !important;
}

/* ----- Sidebar (Dark wood theme) ----- */
.css-1d391kg, .css-1avcm0n {
    background: rgba(30, 20, 10, 0.85) !important;
    color: #e9ddc6 !important;
}

.css-1lcbmhc, .css-17lntkn {
    color: #e9ddc6 !important;
}

/* Sidebar buttons */
.css-1q8dd3e, .css-1x8cf1d {
    background-color: #6d4c32 !important;
    color: #fff8e6 !important;
    border-radius: 6px !important;
}

/* Title Styles */
h1, h2, h3, h4 {
    font-family: "Georgia", serif !important;
    color: #f8e9c8 !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
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
