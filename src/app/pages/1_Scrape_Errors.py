import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Scrape Errors",
    page_icon="⚠️",
    layout="wide"
)

st.title("Scrape Errors")
st.caption("Logs of funds and rows that failed validation or threw errors during daily scraping.")


def get_errors_file() -> Path:
    candidates = [
        Path("data/scrape_errors.csv"),
        Path(__file__).resolve().parents[3] / "data" / "scrape_errors.csv",
        Path(__file__).resolve().parents[2] / "data" / "scrape_errors.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    return Path("data/scrape_errors.csv")


errors_file = get_errors_file()

with st.sidebar:
    st.subheader("Navigation")
    st.page_link("main.py", label="Performance Comparison", icon="📈")
    st.page_link("pages/1_Scrape_Errors.py", label="Scrape Errors", icon="⚠️")
    st.divider()
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if not errors_file.exists() or errors_file.stat().st_size == 0:
    st.info("ℹ️ No scrape errors found. `data/scrape_errors.csv` is empty or has not been generated yet.")
else:
    try:
        df = pd.read_csv(errors_file)

        # Standard expected columns
        expected_cols = ['fund_name', 'date', 'raw_value']

        # Handle legacy or missing headers
        if not all(col in df.columns for col in expected_cols):
            df_no_header = pd.read_csv(errors_file, header=None)
            if df_no_header.shape[1] >= 3:
                df = df_no_header.iloc[:, :3]
                df.columns = expected_cols
            elif df_no_header.shape[1] == 2:
                df = df_no_header.iloc[:, :2]
                df.columns = ['fund_name', 'raw_value']
                df['date'] = 'N/A'
                df = df[expected_cols]

        if df.empty:
            st.success("🎉 No scrape errors recorded! All funds scraped cleanly.")
        else:
            # Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Error Entries", len(df))
            with m2:
                st.metric("Unique Affected Funds", df['fund_name'].nunique())
            with m3:
                latest_date = df['date'].dropna().max() if 'date' in df.columns and not df['date'].dropna().empty else "N/A"
                st.metric("Latest Error Date", str(latest_date))

            st.divider()

            # Filters
            col_search, col_filter = st.columns([2, 1])
            with col_search:
                search_query = st.text_input("🔍 Search by Fund Name", placeholder="Type to filter...")
            with col_filter:
                unique_dates = sorted(df['date'].dropna().astype(str).unique().tolist(), reverse=True)
                selected_dates = st.multiselect("Filter by Date", options=unique_dates, default=[])

            filtered_df = df.copy()
            if search_query:
                filtered_df = filtered_df[filtered_df['fund_name'].astype(str).str.contains(search_query, case=False, na=False)]
            if selected_dates:
                filtered_df = filtered_df[filtered_df['date'].astype(str).isin(selected_dates)]

            st.dataframe(
                filtered_df,
                use_container_width=True,
                column_config={
                    "fund_name": st.column_config.TextColumn("Fund Name"),
                    "date": st.column_config.TextColumn("Date"),
                    "raw_value": st.column_config.TextColumn("Raw Scraped Value"),
                },
                hide_index=True,
            )

            # Export button
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Errors (CSV)",
                data=csv_data,
                file_name="scrape_errors_export.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error reading `data/scrape_errors.csv`: {e}")
