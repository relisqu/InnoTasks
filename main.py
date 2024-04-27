#!/usr/bin/python
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import hashlib
import database.settings
from database.db import *

# Data Viz Pkgs

import plotly.express as px

HTML_BANNER = \
    """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">ToDo App (CRUD)</h1>
    <p style="color:white;text-align:center;">Built with Streamlit</p>
    </div>
    """

# Global variable to store user ID



login_menu = st.empty()
create_table()
def login():
	with login_menu.container():
		stc.html(HTML_BANNER)

		st.subheader('Login')
		username = st.text_input('Username')
		password = st.text_input('Password', type='password')

		if st.button('Login'):
			password_hash = \
				hashlib.sha256(password.encode()).hexdigest()
			user = authenticate_user(username, password_hash)
			if user:
				database.settings.user_id = user[0]  # Set user_id
				st.success('Logged in successfully!')
			else:
				st.error('Invalid username or password')

		if st.button('Register'):
            
			if get_user_by_username(username):
				st.error('Username already exists. Please choose a different one.')
			else:
				password_hash = \
					hashlib.sha256(password.encode()).hexdigest()
				register_user(password, password_hash)
				st.success('Registration successful! You can now login.')


if database.settings.user_id  is not None:
	if st.button('Logout'):
		database.settings.user_id = None
		st.rerun()
else:
	login()