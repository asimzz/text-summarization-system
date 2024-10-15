import os
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Base URL for the FastAPI app
api_url = os.getenv("API_BASE_URL")

# Function for registration
def register_user():
    st.title("User Registration")
    
    # Adding full name and role fields as required by FastAPI
    full_name = st.text_input("Full Name", key="full_name")
    role = st.selectbox("Role", ["user", "Admin"], key="role")  # Example roles, you can customize
    
    username = st.text_input("Username", key="username")
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="password")
    
    if st.button("Register", key="register"):
        # Prepare the data, including the required fields
        data = {
            "full_name": full_name,
            "role": role,
            "username": username,
            "email": email,
            "password": password,
            "created_at": datetime.now().isoformat()  # Automatically set the current timestamp
        }
        
        response = requests.post(f"{api_url}/register", json=data)
        
        if response.status_code == 200:
            st.success("User registered successfully!")
        else:
            # Extracting and displaying the error message(s)
            error_detail = response.json().get("detail", "Registration failed")
            if isinstance(error_detail, list):
                error_message = " | ".join([str(item) for item in error_detail])
            else:
                error_message = str(error_detail)
                
            st.error("Error: " + error_message)

# Function for login
def login_user():
    st.title("Login")
    
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", key="login"):
        data = {"username": username, "password": password}
        response = requests.post(f"{api_url}/login", json=data)
        
        if response.status_code == 200:
            st.success("Login successful!")
            token = response.json()["access_token"]
            st.session_state["token"] = token
        else:
            st.error("Login failed: " + response.json().get("detail", "Invalid credentials"))

# Function for text summarization
def summarize_text():
    st.title("Text Summarization")
    
    if "token" not in st.session_state:
        st.warning("Please log in to use the summarization service.")
        return
    
    text = st.text_area("Enter text to summarize", key="summarize_text")
    
    if st.button("Summarize", key="summarize_button"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        data = {"text": text}
        
        # Send the request to FastAPI
        response = requests.post(f"{api_url}/summarize", json=data, headers=headers)
        
        if response.status_code == 200:
            summary = response.json()["summary_text"]  # Get the plain text response
            st.write("Summary:", summary)
        else:
            st.error("Error: " + response.text)  # Handle the error as text


# Sidebar navigation with unique keys for each radio element
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Register", "Login", "Summarize"], key="navigation_radio")

if choice == "Register":
    register_user()

elif choice == "Login":
    login_user()

elif choice == "Summarize":
    summarize_text()
