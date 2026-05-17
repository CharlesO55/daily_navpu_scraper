import streamlit as st

st.title("Performance Comparssion")


from app_state import initialize_session_state

from elements.sidebar.sidebar import sidebar



initialize_session_state()

sidebar()



if st.session_state['df_main'] is not None:
    st.subheader("Price")
    st.divider()
    st.line_chart(data=st.session_state['df_main'], x='date', y='value', color='fund_name')


    st.dataframe(st.session_state['df_main'])
    # st.subheader("Daily Change")
    # st.divider()
    # st.line_chart(data=st.session_state['df_main'], x='date', y='cumulative_return', color='fund_name')


    # # st.dataframe(df_delta.pivot(index='date', columns='fund_name', values='cumulative_return'))