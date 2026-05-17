import streamlit as st
from itertools import chain

from utils.file_loader import get_bank_uitf_funds_list , build_df_from_uitf_funds
from utils.calculate_df import calculate_daily_delta , mask_date_range


def menu_uitf():
    with st.expander("UITF Funds", expanded=True):
        uitf_list = get_bank_uitf_funds_list()
        
        selected_banks = st.multiselect(
            "1. Select Bank(s)", 
            options=sorted(uitf_list.keys()),
            default=['chinabank']
        )
        selected_banks = sorted(selected_banks)

        available_funds = list(chain.from_iterable(
            uitf_list[bank] for bank in selected_banks
        ))

        selected_funds = st.multiselect(
            "2. Select Fund(s)", 
            options=available_funds,
            format_func=lambda x : x.get("name"),
        )



        if selected_funds:
            df = build_df_from_uitf_funds(selected_funds)
            df = mask_date_range(df)
            df = calculate_daily_delta(df)

            st.session_state['df_main'] = df