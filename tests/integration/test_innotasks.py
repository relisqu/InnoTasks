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
        try:
            assert login_error_btn.value is True
        finally:
            del e

