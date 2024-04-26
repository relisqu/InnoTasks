import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import hashlib
import database.settings
from database.db import *

user_id = database.settings.user_id
if(user_id is None):
      st.text("Please login")
st.subheader('Edit Items')
with st.expander('Current Data'):
            result = view_all_data(user_id)

            # st.write(result)

            clean_df = pd.DataFrame(result, columns=['Task', 'Status',
                                    'Date'])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names(user_id)]
        selected_task = st.selectbox('Task', list_of_tasks)
        task_result = get_task(user_id, selected_task)

        # st.write(task_result)

        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            (col1, col2) = st.columns(2)

            with col1:
                new_task = st.text_area('Task To Do', task)

            with col2:
                new_task_status = st.selectbox(task_status, ['ToDo',
                        'Doing', 'Done'])
                new_task_due_date = st.date_input(task_due_date)

            if st.button('Update Task'):
                edit_task_data(
                    user_id,
                    new_task,
                    new_task_status,
                    new_task_due_date,
                    task,
                    task_status,
                    task_due_date,
                    )
                st.success('Updated ::{} ::To {}'.format(task,
                           new_task))

            with st.expander('View Updated Data'):
                result = view_all_data(user_id)

                # st.write(result)

                clean_df = pd.DataFrame(result, columns=['Task',
                        'Status', 'Date'])
                st.dataframe(clean_df)