import streamlit as st
from datetime import date

'''
    A sidebar container with date range selection.
'''

def menu_date():
    with st.container(border=True):
        st.subheader("Range")
        
        cols = st.columns(2)
        
        with cols[0]:
            st.date_input(
                label="Start Date",
                key="date_start",
                max_value=date.today()
            )

        with cols[1]:
            st.date_input(
                label="End Date",
                key="date_end",
                max_value=date.today()
            )