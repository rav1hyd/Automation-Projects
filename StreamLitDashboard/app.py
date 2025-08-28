import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from io import BytesIO
import plotly.graph_objects as go
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# --- Page Config ---
st.set_page_config(page_title="Server Patching Dashboard", layout="wide")

# --- Load credentials from YAML ---
with open("StreamLitDashboard/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# --- Login Form ---
authenticator.login(location="main")

# --- Check login status ---
if st.session_state["authentication_status"]:
    # --- Logout in sidebar ---
    authenticator.logout(location="sidebar")

    st.success(f"Welcome {st.session_state['name']} 👋")

    st.title("🔧 Server Patching Dashboard")

    # --- Functions ---
    def patch_server(_server_row):
        """Simulate patching process with random results."""
        time.sleep(0.2)  # simulate work
        return random.choice(["Patched", "Failed", "Connectivity Issue"])

    def status_badge(status: str) -> str:
        """Return colored HTML badge for status."""
        color_map = {
            "Patched": "green",
            "Failed": "red",
            "Connectivity Issue": "orange",
            "Pending": "gray",
        }
        color = color_map.get(status, "gray")
        return f"<span style='color:white; background-color:{color}; padding:4px 8px; border-radius:8px;'>{status}</span>"

    REQUIRED_COLUMNS = {"Hostname", "IP Address", "OS Type", "OS Version"}

    def validate_columns(df: pd.DataFrame) -> bool:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            st.error(f"Your Excel is missing columns: {', '.join(sorted(missing))}")
            return False
        return True

    # --- Sidebar ---
    st.sidebar.header("Actions")
    st.sidebar.write("1️⃣ Upload Excel → 2️⃣ Run Simulation → 3️⃣ Filter / Export Results")

    # --- File Upload ---
    uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if not validate_columns(df):
            st.stop()

        st.subheader("📋 Uploaded Server List")
        st.dataframe(df, use_container_width=True)

        # --- Run full patching simulation ---
        if st.button("🚀 Run Patching Simulation", use_container_width=True):
            with st.spinner("Running patch simulation..."):
                df["Status"] = df.apply(patch_server, axis=1)

            st.session_state["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state["df"] = df

        # --- Re-run only failed servers ---
        if st.button("🔄 Re-run Failed Servers Only", use_container_width=True):
            if "df" in st.session_state:
                df = st.session_state["df"]
                with st.spinner("Re-running failed servers..."):
                    df.loc[df["Status"] == "Failed", "Status"] = df[df["Status"] == "Failed"].apply(patch_server, axis=1)
                st.session_state["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["df"] = df
            else:
                st.warning("⚠️ Please run a full simulation first.")

        # --- If results exist, show dashboard ---
        if "df" in st.session_state:
            df = st.session_state["df"]

            # Save to buffer for download
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)

            # --- KPI Cards ---
            st.subheader("📊 Patch Summary")
            total = len(df)
            patched = (df["Status"] == "Patched").sum()
            failed = (df["Status"] == "Failed").sum()
            conn_issues = (df["Status"] == "Connectivity Issue").sum()
            pending = (df["Status"] == "Pending").sum()
            compliance = (patched / total * 100) if total > 0 else 0

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Total Servers", total)
            col2.metric("✅ Patched", patched)
            col3.metric("❌ Failed", failed)
            col4.metric("⚠️ Connectivity", conn_issues)
            col5.metric("⏳ Pending", pending)

            if "last_run" in st.session_state:
                st.caption(f"Last run: {st.session_state['last_run']}")

            # --- Compliance Gauge ---
            st.subheader("📈 Compliance Overview")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=compliance,
                title={"text": "Patch Compliance %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 50], "color": "red"},
                        {"range": [50, 80], "color": "orange"},
                        {"range": [80, 100], "color": "green"},
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

            # --- Filters (combined selection) ---
            st.subheader("🔎 Filter View")
            os_options = df["OS Type"].unique().tolist()
            status_options = df["Status"].unique().tolist()

            selected_os = st.multiselect("Select OS Type(s)", os_options)
            selected_status = st.multiselect("Select Status(es)", status_options)

            df_filtered = df.copy()
            if selected_os:
                df_filtered = df_filtered[df_filtered["OS Type"].isin(selected_os)]
            if selected_status:
                df_filtered = df_filtered[df_filtered["Status"].isin(selected_status)]

            # --- Detailed Table with Badges ---
            df_display = df_filtered.copy()
            df_display["Status"] = df_display["Status"].apply(status_badge)
            st.markdown(
                df_display.to_html(escape=False, index=False),
                unsafe_allow_html=True,
            )

            # --- Drill-down View ---
            st.subheader("🔍 Server Details")
            selected_server = st.selectbox("Select a server", df_filtered["Hostname"])
            server_data = df[df["Hostname"] == selected_server].copy()
            server_data["Status"] = server_data["Status"].apply(status_badge)
            st.write(server_data.to_html(escape=False, index=False), unsafe_allow_html=True)

            # --- Download Updated Excel ---
            st.download_button(
                "⬇️ Download Updated Excel",
                data=buffer,
                file_name=f"updated_servers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
