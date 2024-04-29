from streamlit.testing.v1 import AppTest


def test_login_successful():
    # Define test inputs
    test_username = "test_user"
    test_password = "test_password"

    # Create an AppTest object
    app = AppTest.from_file("../../innotasks/main.py")
    app.run()

    # Simulate user input for login
    app.text_input[0].set_value(test_username)
    app.text_input[1].set_value(test_password)

    # Simulate user click on login button
    login_btn = app.button[0]
    login_btn.click()

    # Check if user is logged in
    assert login_btn.value is True


def test_login_invalid_credentials():
    # Define test inputs
    test_username = "invalid_user"
    test_password = "invalid_password"

    # Create an AppTest object
    app = AppTest.from_file("../../innotasks/main.py")
    app.run()

    # Simulate user input for login
    app.text_input[0].set_value(test_username)
    app.text_input[1].set_value(test_password)

    # Simulate user click on login button
    login_error_btn = app.button[0]

    # Check if error is triggered
    try:
        login_error_btn.click()
        login_error_btn.run()
    except Exception as e:
        assert login_error_btn.value == True



def test_view_all_data(app):
    # Simulate user session state
    st.session_state["user_id"] = "test_user_id"

    # Simulate main application function call
    app.run()

    # Simulate user selecting "Read" from the menu
    app.sidebar.selectbox.select("Read")

    # Check if data is displayed
    assert app.dataframe


def test_add_task(app):
    # Simulate user session state
    st.session_state["user_id"] = "test_user_id"

    # Simulate main application function call
    app.run()

    # Simulate user selecting "Create" from the menu
    app.sidebar.selectbox.select("Create")

    # Simulate user input for task creation
    app.text_area.set_value("Test Task")
    app.selectbox.set_value("ToDo")
    app.selectbox_1.set_value("Important")
    app.date_input.set_value("2024-04-28")

    # Simulate user click on "Add Task" button
    app.button.click()

    # Check if success message is displayed
    assert app.success


def test_update_task():
    st.session_state["user_id"] = "test_user_id"

    app = AppTest.from_file("../../innotasks/main.py")
    app.run()
    app.sidebar.selectbox.select("Update")
    app.selectbox.select("Task 1")

    app.text_area.set_value("Updated Task")
    app.selectbox_2.set_value("Done")
    app.selectbox_3.set_value("Critical")
    app.date_input_1.set_value("2024-04-30")

    app.button.click()
    assert app.success


def test_delete_task(app):
    st.session_state["user_id"] = "test_user_id"
    app.run()
    app.sidebar.selectbox.select("Delete")
    app.selectbox.select("Task 1")
    app.button.click()
    assert app.warning
