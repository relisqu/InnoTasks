import streamlit as st
import pandas as pd
import streamlit.components.v1 as stc
import hashlib
import database.settings
from database.db import *


user_id = database.settings.user_id
print(user_id)
if(user_id is None):
      st.text("Please login")
else:
    result = view_all_data(database.settings.user_id)

                # st.write(result)

    clean_df = pd.DataFrame(result, columns=['Task', 'Status',
                                        'Date'])
    st.dataframe(clean_df)