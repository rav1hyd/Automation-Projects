import streamlit as st
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
from modules.utils import status_badge

def show_summary(df):
    """Show KPIs and compliance gauge."""
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

    st.caption(f"Last run: {st.session_state.get('last_run', 'N/A')}")

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

def show_filter(df):
    """Unified filter for OS & Status."""
    st.subheader("🔎 Filter View")
    options = st.multiselect("Filter by OS / Status", 
                             df["OS Type"].unique().tolist() + df["Status"].unique().tolist())
    
    df_filtered = df.copy()
    if options:
        df_filtered = df_filtered[
            df_filtered["OS Type"].isin(options) | df_filtered["Status"].isin(options)
        ]

    df_display = df_filtered.copy()
    df_display["Status"] = df_display["Status"].apply(status_badge)
    st.markdown(
        df_display.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
    return df_filtered

def show_download(df):
    """Download updated Excel."""
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        "⬇️ Download Updated Excel",
        data=buffer,
        file_name=f"updated_servers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
