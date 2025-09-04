import streamlit as st
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
import pandas as pd

def build_condensed(df: pd.DataFrame) -> pd.DataFrame:
    """One row per host: Hostname | Status | OS Type | Output | Details."""
    rows = []
    for host in df["Hostname"].unique():
        host_df = df[df["Hostname"] == host]

        # OS Type
        os_vals = host_df["OS Type"].dropna().unique()
        os_type = os_vals[0] if len(os_vals) else "Unknown"

        # overall status
        all_ok = (host_df["Status"] == "OK").all()
        any_error = host_df["Status"].astype(str).str.contains("Error", na=False).any()
        overall = "OK" if all_ok else ("Error" if any_error else "Pending")

        # representative output (SSH Executor if present)
        if "SSH Executor" in host_df["Module"].values:
            out_vals = host_df.loc[host_df["Module"]=="SSH Executor","Output"].astype(str).values
            output = out_vals[0] if len(out_vals) else ""
        else:
            output = ""

        # details: list only non-OK modules
        issues = []
        for _, r in host_df.iterrows():
            s = str(r["Status"])
            if s == "OK":
                continue
            if s == "Pending" or "Error" in s or "failed" in s.lower():
                short = s.replace("Connection failed:", "").strip()
                issues.append(f"• {r['Module']}: {short or 'Issue'}")
        details = "All checks passed ✅" if not issues else "\n".join(issues)

        rows.append({
            "Hostname": host,
            "Status": overall,
            "OS Type": os_type,
            "Output": output,
            "Details": details,
        })
    return pd.DataFrame(rows)

def show_results_with_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Single widget: filters on top, table below (shows all by default).
    Returns filtered condensed dataframe.
    """
    st.subheader("📊 Results")

    condensed = build_condensed(df)

    # --- filters (default = all selected) ---
    c1, c2, c3 = st.columns([1,1,2])
    os_options = sorted([x for x in condensed["OS Type"].dropna().unique().tolist()])
    status_options = sorted(condensed["Status"].unique().tolist())
    # user sees all rows initially
    sel_os = c1.multiselect("Filter by OS Type", os_options, default=os_options)
    sel_status = c2.multiselect("Filter by Status", status_options, default=status_options)
    # optional quick search by host
    q = c3.text_input("Search Hostname", "")

    # if user clears everything, treat as 'all'
    if not sel_os: sel_os = os_options
    if not sel_status: sel_status = status_options

    filtered = condensed[
        condensed["OS Type"].isin(sel_os) &
        condensed["Status"].isin(sel_status)
    ]
    if q.strip():
        filtered = filtered[filtered["Hostname"].str.contains(q.strip(), case=False, na=False)]

    st.dataframe(filtered, use_container_width=True)
    return filtered

def show_download(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button(
        "⬇️ Download Results (Excel)",
        data=buffer,
        file_name=f"healthcheck_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
