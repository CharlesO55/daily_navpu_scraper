import streamlit as st
import plotly.express as px

st.title("Performance Comparssion")


from app_state import initialize_session_state

from elements.sidebar.sidebar import sidebar



initialize_session_state()

sidebar()



if st.session_state['df_main'] is not None and not st.session_state['df_main'].empty:
    st.subheader("Price")
    st.divider()

    fig = px.line(
        st.session_state['df_main'],
        x='date',
        y='cumulative_return',
        color='fund_name',
        labels={
            'date': 'Date',
            'cumulative_return': 'Cumulative Return',
            'fund_name': 'Fund',
        },
    )
    fig.update_yaxes(tickformat='.2%')
    fig.update_traces(hovertemplate='%{y:.2%}')
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Date',
        yaxis_title='Cumulative Return',
        legend_title_text='Fund',
    )

    st.plotly_chart(fig, use_container_width=True)

    def calc_pct_change(series):
        return 100 * (series.iloc[-1] - series.iloc[0]) / series.iloc[0]

    # st.dataframe(st.session_state['df_main'])

    df_agg_prices = st.session_state['df_main'].groupby('fund_name')['value'].agg(
        pct_change=calc_pct_change,
        price_history=list,
    )

    st.dataframe(df_agg_prices, column_config={
        'fund_name' : st.column_config.TextColumn('Fund'),
        'pct_change' : st.column_config.NumberColumn('Change', format='%.2f'),
        'price_history' : st.column_config.LineChartColumn('Raw Price'),
    })