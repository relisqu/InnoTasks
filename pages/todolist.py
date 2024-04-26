import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import hashlib
from database.db import *



##dont use, use for copypaste etc
def main_application(user_id):
    menu = ['Read', 'Create', 'Update', 'Delete', 'About']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Read':

        # st.subheader("View Items")

        with st.expander('View All'):
            result = view_all_data(user_id)

            # st.write(result)

            clean_df = pd.DataFrame(result, columns=['Task', 'Status',
                                    'Date'])
            st.dataframe(clean_df)

        with st.expander('Task Status'):
            task_df = clean_df['Status'].value_counts().to_frame()

            # st.dataframe(task_df)

            task_df = task_df.reset_index()
            st.dataframe(task_df)

            p1 = px.pie(task_df, names='index', values='Status')
            st.plotly_chart(p1, use_container_width=True)
    elif choice == 'Update':

    elif choice == 'Delete':

        st.subheader('Delete')
        with st.expander('View Data'):
            result = view_all_data(user_id)

            # st.write(result)

            clean_df = pd.DataFrame(result, columns=['Task', 'Status',
                                    'Date'])
            st.dataframe(clean_df)

        unique_list = [i[0] for i in view_all_task_names(user_id)]
        delete_by_task_name = st.selectbox('Select Task', unique_list)
        if st.button('Delete'):
            delete_data(user_id, delete_by_task_name)
            st.warning("Deleted: '{}'".format(delete_by_task_name))

        with st.expander('Updated Data'):
            result = view_all_data(user_id)

            # st.write(result)

            clean_df = pd.DataFrame(result, columns=['Task', 'Status',
                                    'Date'])
            st.dataframe(clean_df)
