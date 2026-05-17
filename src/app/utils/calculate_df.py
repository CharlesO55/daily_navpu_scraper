import pandas as pd
import streamlit as st


def calculate_daily_delta(df_raw : pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()  
    
    df['pct_change'] = df.groupby('fund_name')['value'].pct_change()

    df['cumulative_return'] = df.groupby('fund_name')['pct_change'].transform(
        lambda x: (1 + x.fillna(0)).cumprod() - 1
    )

    return df


def mask_date_range(df : pd.DataFrame) -> pd.DataFrame:
    date_mask = df['date'].between(st.session_state.get('date_start'), st.session_state.get('date_end'))
    return df[date_mask]


def append_fund_history(df : pd.DataFrame) -> None:
    df_original = st.session_state.get('df_main')
    funds_to_add = df['fund_name'].unique()

    mask = ~ df_original['fund_name'].isin(funds_to_add)

    st.session_state['df_main'] = pd.concat([df_original[mask], df])