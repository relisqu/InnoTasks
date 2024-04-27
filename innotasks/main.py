import os

import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import requests
from os import environ
import subprocess
# Data Viz Pkgs
import plotly.express as px
from datetime import datetime
from repository.repository import add_task, view_all_task_names, get_task, edit_task_data, delete_data

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Stans Team</p>
    </div>
    """


login_menu = st.empty()


def main_login():
    with login_menu.container():
        stc.html(HTML_BANNER)

        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                user = login(username, password)
                print(user)
                if user:
                    user_id = user[0]
                    st.session_state['user_id'] = user_id # Set the user ID
                    st.success("Logged in successfully!")
                    login_menu.empty()  # Clear the login menu
                    main_application(user_id)
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter username and password")

        if st.button("Register"):
            if username and password:
                response = register(username, password)
                if response:
                    st.success("Registered successfully!")
                else:
                    st.error("User already exists")
            else:
                st.warning("Please enter username and password")


def main_application(user_id):
    stc.html(HTML_BANNER)

    menu = ["Read", "Create", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create":
        st.subheader("Add Item")
        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_priority = st.selectbox('Priority', ['Not important', 'Important','Very important','Critical'])
            task_due_date = str(st.date_input("Due Date"))

        if st.button("Add Task"):
            add_task(user_id, task, task_status, task_priority, task_due_date)
            st.success("Added ::{} ::To Task".format(task))

    elif choice == "Read":
        st.subheader("View Items")
        with st.expander("View All"):
            result = view_all_data(user_id)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", 'Priority', "Date"])
            st.dataframe(clean_df)

        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()
            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='count', values='Status')
            st.plotly_chart(p1, use_container_width=True)

    elif choice == "Update":
        st.subheader("Edit Items")

        list_of_tasks = view_all_task_names(user_id)
        selected_task = st.selectbox("Task", options=list_of_tasks, format_func=lambda x: x[0])

        task_id = selected_task[1]
        task_result = get_task(user_id, task_id)

        if task_result:
            task_id, _, task_name, task_status, task_priority, task_due_date_str = task_result[0]
            task_due_date = datetime.strptime(task_due_date_str, "%Y-%m-%d").date()

            col1, col2 = st.columns(2)

            with col1:
                new_task_name = st.text_area("Task To Do", task_name)

            with col2:
                new_task_status = st.selectbox('Status', ["ToDo", "Doing", "Done"])
                new_task_priority = st.selectbox('Priority', ['Not important', 'Important','Very important','Critical'])
                new_task_due_date = str(st.date_input(label="Due Date", value=task_due_date))

            if st.button("Update Task"):
                edit_task_data(user_id, task_id, new_task_name, new_task_status, new_task_priority, new_task_due_date)
                st.success("Updated ::{} ::To {}".format(task_name, new_task_name))

    elif choice == "Delete":
        st.subheader("Delete")

        list_of_tasks = view_all_task_names(user_id)
        selected_task = st.selectbox("Select Task", options=list_of_tasks, format_func=lambda x: x[0])
        [task_name, task_id] = selected_task

        if st.button("Delete"):
            delete_data(user_id, task_id)
            st.warning("Deleted: '{}'".format(task_name))


url = environ.get("API_URL")


# Function to send a register request to FastAPI
def register(username, password):
    endpoint = f"{url}/register"
    payload = {"username": username, "password": password}
    resp = requests.post(endpoint, json=payload)
    if resp.status_code == 200:
        return resp.json()
    raise ValueError(f"{resp.status_code}: {resp.text}")


# Function to send a login request to FastAPI
def login(username, password):
    endpoint = f"{url}/login"
    payload = {"username": username, "password": password}
    response = requests.post(endpoint, json=payload)
    print(f"resp login: {response}")
    if response.status_code == 200:
        print(f"resp json: {response.json()}")
        return response.json()
    raise ValueError("Invalid username or password")

def view_all_data(user_id):
    endpoint = f"{url}/tasks/{user_id}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()

    raise ValueError("Something got wrong :(", response.status_code)


if __name__ == '__main__':
    if url is None:
        st.warning("API_URL environment variable not set.")

    # Check from session state whether user is authenticated
    if 'user_id' not in st.session_state:
        main_login()
    else:
        user_id = st.session_state['user_id']
        main_application(user_id)
