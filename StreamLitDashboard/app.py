import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

from modules.file_handler import load_excel
from modules.dashboard import show_summary, show_filter, show_download
from main_runner import run_all

# --- Page Config ---
st.set_page_config(page_title="Server Health Dashboard", layout="wide")

# --- Load credentials ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# --- Login Form ---
authenticator.login(location="main")

# --- If logged in ---
if st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar")
    st.success(f"Welcome {st.session_state['name']} 👋")
    st.title("🔧 Server Health Dashboard")
    # --- Sidebar --- 
    st.sidebar.header("Actions") 
    st.sidebar.write("1️⃣ Upload Excel → 2️⃣ Run Health Checks → 3️⃣ Filter / Export Results")

    # Upload Excel
    uploaded_file = st.file_uploader("📂 Upload Server Excel", type=["xlsx", "xls"])

    if uploaded_file:
        df = load_excel(uploaded_file)   # ✅ use file_handler.py
        st.subheader("📋 Uploaded Server List")
        st.dataframe(df, use_container_width=True)

        # Run modules
        if st.button("🚀 Run Health Checks", use_container_width=True):
            with st.spinner("Running all modules..."):
                results_df = run_all(uploaded_file)
            st.session_state["results_df"] = results_df

        # Show dashboard
        if "results_df" in st.session_state:
            results_df = st.session_state["results_df"]

            show_summary(results_df)
            filtered = show_filter(results_df)
            show_download(filtered)

# --- Auth failures ---
elif st.session_state["authentication_status"] is False:
    st.error("❌ Username/password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("⚠️ Please enter your username and password")
