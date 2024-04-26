import os

import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import requests
from os import environ
import subprocess
# Data Viz Pkgs
import plotly.express as px

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """

# Global variable to store user ID
user_id = None

login_menu = st.empty()


def main():
    global user_id

    with login_menu.container():
        stc.html(HTML_BANNER)

        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                user = login(username, password)
                if user:
                    user_id = user[0]  # Set user_id
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

    menu = ["Read", "Create", "Update", "Delete", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create":
        st.subheader("Add Item")
        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["ToDo", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            req.add_task(user_id, task, task_status, task_due_date)
            st.success("Added ::{} ::To Task".format(task))

    elif choice == "Read":
        # st.subheader("View Items")
        with st.expander("View All"):
            result = view_all_data(user_id)
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame()
            # st.dataframe(task_df)
            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='index', values='Status')
            st.plotly_chart(p1, use_container_width=True)

    elif choice == "Update":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data(user_id)
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names(user_id)]
        selected_task = st.selectbox("Task", list_of_tasks)
        task_result = get_task(user_id, selected_task)
        # st.write(task_result)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)

            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ["ToDo", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(user_id, new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success("Updated ::{} ::To {}".format(task, new_task))

            with st.expander("View Updated Data"):
                result = view_all_data(user_id)
                # st.write(result)
                clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                st.dataframe(clean_df)

    elif choice == "Delete":
        st.subheader("Delete")
        with st.expander("View Data"):
            result = view_all_data(user_id)
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        unique_list = [i[0] for i in view_all_task_names(user_id)]
        delete_by_task_name = st.selectbox("Select Task", unique_list)
        if st.button("Delete"):
            delete_data(user_id, delete_by_task_name)
            st.warning("Deleted: '{}'".format(delete_by_task_name))

        with st.expander("Updated Data"):
            result = view_all_data(user_id)
            # st.write(result)
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)


url = environ.get("API_URL")


# Function to send a register request to FastAPI
def register(username, password):
    endpoint = f"{url}/register"
    payload = {"username": username, "password": password}
    resp = requests.post(endpoint, json=payload)
    return resp.json()


# Function to send a login request to FastAPI
def login(username, password):
    endpoint = f"{url}/login"
    payload = {"username": username, "password": password}
    response = requests.post(endpoint, json=payload)
    return response.json()


def add_task(user_id, task, task_status, task_due_date):
    endpoint = f"{url}/task"
    payload = {"user_id": user_id, "task": task, "task_status": task_status, "task_due_date": task_due_date}
    response = requests.post(endpoint, json=payload)
    return response.json()


if __name__ == '__main__':
    if url is None:
        st.warning("API_URL environment variable not set.")
    main()
