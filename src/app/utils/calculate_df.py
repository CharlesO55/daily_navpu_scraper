import streamlit as st


def calculate_daily_delta(df_raw):
    df = df_raw.copy()  
    
    df['pct_change'] = df.groupby('fund_name')['value'].pct_change()

    df['cumulative_return'] = df.groupby('fund_name')['pct_change'].transform(
        lambda x: (1 + x.fillna(0)).cumprod() - 1
    )

    return df