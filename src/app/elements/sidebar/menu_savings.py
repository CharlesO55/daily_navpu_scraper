import streamlit as st


# df_main = pd.DataFrame(columns=['Date', 'Name', 'Value']).astype({
#     'Date': 'datetime64[ns]',
#     'Name': 'string',
#     'Value': 'float32'
# })
 


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
            _rate = td_net_rate / 365