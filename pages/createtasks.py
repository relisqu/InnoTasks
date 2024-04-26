import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import hashlib
import database.settings
from database.db import *

if(database.settings.user_id is None):
      st.text("Please login")
else:
    st.subheader('Add Item')
    (col1, col2) = st.columns(2)

    with col1:
        task = st.text_area('Task To Do')

    with col2:
        task_status = st.selectbox('Status', ['ToDo', 'Doing','Done'])
        task_priority = st.selectbox('Status', ['Not important', 'Important','Very important','Critical'])
        task_due_date = st.date_input('Due Date')

        if st.button('Add Task'):
            add_data(database.settings.user_id, task, task_status,task_priority, task_due_date)
            st.success('Added :: {} :: to task list'.format(task))