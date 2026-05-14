import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta



def initialize_session_state():
    """Defines all global defaults in one place."""
    defaults = {
        'date_start': date.today() - relativedelta(months=1),
        'date_end': date.today(),
        'df_main': None,  
        'increment_val': 1.0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value



def reset_session_state():
    filter_keys = ['date_start', 'date_end', 'increment_val']
    for key in filter_keys:
        if key in st.session_state:
            del st.session_state[key]

    initialize_session_state()
    st.rerun()