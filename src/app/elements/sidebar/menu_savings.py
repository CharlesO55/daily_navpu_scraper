import streamlit as st
import pandas as pd

from utils.calculate_df import calculate_daily_delta, mask_date_range, append_fund_history


def menu_savings():
    with st.expander("Savings/TD", expanded=True):
        td_gross_rate = st.slider(
            label="Annual Gross Rate",
            min_value=0.0,
            max_value=20.0,
            value=6.0,
            step=0.25,      
            format="%.2f" 
        )

        td_net_rate = (td_gross_rate * 0.8) / 100
        st.write(f"Net Rate : {td_net_rate * 100:.2f}%")

        if st.button("Add"):
            def build_simulated_data():
                daily_rate = td_net_rate / 365

                dates = pd.date_range(start=st.session_state.get('date_start'), end=st.session_state.get('date_end'), freq='D').date

                days = len(dates)

                values = [1 + (i * daily_rate) for i in range(days)]
                
                return pd.DataFrame({
                    'date': dates,
                    'fund_name' : f'Benchmark ({td_gross_rate:.2f}%)',
                    'value': values
                })


            df = build_simulated_data()
            df = mask_date_range(df)
            df = calculate_daily_delta(df)
            append_fund_history(df)