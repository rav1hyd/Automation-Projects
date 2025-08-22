import streamlit as st
import pandas as pd

REQUIRED_COLUMNS = {"Hostname", "IP Address", "OS Type", "OS Version"}

def upload_excel():
    """Upload and validate Excel file, return DataFrame if valid."""
    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
            return None
        return df
    else:
        st.info("Upload an Excel file to begin. Sample: `servers.xlsx`")
        return None
