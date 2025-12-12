import streamlit as st
from datetime import datetime
import uuid
def set_study_gradient():
    st.markdown(
        """
        <style>
        /* Full App Background */
        .stApp {
            background: linear-gradient(135deg, #1e3c72, #2a5298, #4c2a85);
            background-attachment: fixed;
        }

        /* Page text styling for readability */
        h1, h2, h3, label, p {
            color: #ffffff !important;
            text-shadow: 0px 2px 5px rgba(0,0,0,0.4);
        }

        /* Input areas styling */
        .stTextInput, .stTextArea {
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 10px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #6a5acd !important;
            color: white !important;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: bold;
            border: 1px solid white;
        }

        /* Button hover */
        .stButton>button:hover {
            background-color: #8a7adc !important;
            border-color: #ffffff;
        }

        /* Response box background */
        .stAlert {
            background-color: rgba(255,255,255,0.2) !important;
            color: white !important;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


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
