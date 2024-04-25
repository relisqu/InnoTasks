import streamlit as st
import pandas as pd 
from db import * 
import streamlit.components.v1 as stc
import hashlib



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
    create_table()

    with login_menu.container():
        stc.html(HTML_BANNER)
        
        # Menu options
        menu = ["Login", "Register", "About"]
        choice = st.sidebar.selectbox("Menu", menu)

        # Flag to control login/register form visibility
        show_login = False
        show_register = False

        if choice == "Login":
            show_login = True
        elif choice == "Register":
            show_register = True

        if show_login:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                user = authenticate_user(username, password_hash)
                if user:
                    user_id = user[0]  # Set user_id
                    st.success("Logged in successfully!") 
                    login_menu.empty()   
                    st.sidebar.empty()             
                    menu = ["Create", "Read", "Update", "Delete"]
                    choice = st.sidebar.selectbox("Menu", menu)
                    return
                else:
                    st.error("Invalid username or password")

        elif show_register:
            st.subheader("Register")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")

            if st.button("Register"):
                # Check if username already exists
                if get_user_by_username(new_username):
                    st.error("Username already exists. Please choose a different one.")
                else:
                    # Hash the password
                    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                    # Register the user
                    register_user(new_username, password_hash)
                    st.success("Registration successful! You can now login.")

        elif choice == "About":
            st.subheader("About")
            st.write("This is a Streamlit ToDo App with CRUD operations.")
        
        # If user is logged in, show the main application
     #   if user_id is not None:
    #     main_application()

def main_application():
    # Main application code for CRUD operations
    st.subheader("Welcome to the ToDo App")
    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Create":
        # Code for adding tasks
        st.write("Create functionality will be implemented here")
        
    elif choice == "Read":
        # Code for reading tasks
        st.write("Read functionality will be implemented here")
        
    elif choice == "Update":
        # Code for updating tasks
        st.write("Update functionality will be implemented here")
        
    elif choice == "Delete":
        # Code for deleting tasks
        st.write("Delete functionality will be implemented here")


def main_application2(user_id):
	stc.html(HTML_BANNER)


	menu = ["Create","Read","Update","Delete","About"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Create":
		st.subheader("Add Item")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_area("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added ::{} ::To Task".format(task))


	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)


	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)



if __name__ == '__main__':
	main()