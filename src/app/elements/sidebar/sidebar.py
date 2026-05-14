import streamlit as st

from elements.sidebar.menu_date import menu_date 
from elements.sidebar.menu_uitf import menu_uitf 
from elements.sidebar.menu_savings import menu_savings

def sidebar():
    with st.sidebar:
        menu_date()
        menu_uitf()
        menu_savings()