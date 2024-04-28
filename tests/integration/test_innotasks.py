import streamlit as st
from streamlit.testing.v1 import AppTest
import pytest

def test_login_successful():
    # Define test inputs
    test_username = "test_user"
    test_password = "test_password"

    # Define expected outputs
    expected_success_message = "Logged in successfully!"

    # Create an AppTest object
    app = AppTest.from_file("../../innotasks/main.py")


    # Simulate user input for login
    app.text_input("Username").value = test_username
    app.text_input("Password").value = test_password
    app.button("Login")

    # Check if success message is displayed
    assert app.success_message == expected_success_message

def test_login_invalid_credentials():
    # Define test inputs
    test_username = "invalid_user"
    test_password = "invalid_password"

    # Define expected outputs
    expected_error_message = "Invalid username or password"

    # Create an AppTest object
    app = AppTest("innotasks/main.py")

    # Simulate user input for login
    app.text_input("Username", value=test_username)
    app.text_input("Password", value=test_password)
    app.button("Login")

    # Check if error message is displayed
    assert app.error_message == expected_error_message

test_login_successful()