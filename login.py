import streamlit as st
import requests

# Streamlit UI
st.title("FastAPI + Streamlit Demo - Login/Register")

# Function to send a register request to FastAPI
def register(username, password):
    url = "http://localhost:8000/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()

# Function to send a login request to FastAPI
def login(username, password):
    url = "http://localhost:8000/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()

# Input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to trigger register
if st.button("Register"):
    if username and password:
        response = register(username, password)
        st.write(response)
    else:
        st.warning("Please enter username and password")

# Button to trigger login
if st.button("Login"):
    if username and password:
        response = login(username, password)
        st.write(response)
    else:
        st.warning("Please enter username and password")