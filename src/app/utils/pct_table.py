import pandas as pd
from typing import Optional

from styles import format_metric , color_metric
import streamlit as st


OFFSETS = [
    { 'text' : 'Daily', 'dt' : pd.DateOffset(days=1) },
    { 'text' : '1 Week', 'dt' : pd.DateOffset(weeks=1) },
    { 'text' : '1 Month', 'dt' : pd.DateOffset(months=1) },
    { 'text' : '3 Months', 'dt' : pd.DateOffset(months=3) },
]

def calculate_latest_changes(group):
    latest_row = group.iloc[-1]
    latest_date = latest_row['date']
    latest_value = latest_row['value']
    

    def get_asof_value(target_date):
        past_data = group[group['date'] <= target_date]
        if not past_data.empty:
            return past_data.iloc[-1]['value']
        return None


    def get_pct_change(val_latest : float, val_prev : Optional[pd.Timestamp]):
        # (New - Old) / Old
        return ((val_latest - val_prev) / val_prev) if val_prev else None


    results = {
        'latest_date': latest_date,
        'latest_value': latest_value,
    }


    for offset in OFFSETS:
        past_date = latest_date - offset['dt']
        pct_change = get_pct_change(latest_value, get_asof_value(past_date))

        results[offset['text']] = pct_change

    return pd.Series(results)




def build_delta_table(df_master) : 
    df = df_master.groupby('fund_name').apply(calculate_latest_changes)
    df.index.name = 'Fund'
    df.rename(
        columns = {
            'latest_date' : 'Date',
            'latest_value' : 'Value',
        },
        inplace=True
    )

    df['Date'] = df['Date'].dt.strftime('%m-%d (') + df['Date'].dt.day_name().str[:3] + ')'

    target_cols = df.columns[2:]

    return st.dataframe(df.style \
        .format(format_metric, subset=target_cols) \
        .map(color_metric, subset=target_cols))