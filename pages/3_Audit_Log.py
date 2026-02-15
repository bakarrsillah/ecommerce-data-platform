import streamlit as st
import pandas as pd
from db import get_engine

# 🔐 Stakeholder Only
if not st.session_state.get("logged_in") or st.session_state.get("role") != "stakeholder":
    st.error("🚫 Access Denied")
    st.stop()

st.title("📜 Audit Log")

engine = get_engine()

df = pd.read_sql("""
    SELECT audit_id,
           username,
           action_type,
           table_name,
           record_id,
           action_time,
           details
    FROM audit_log
    ORDER BY action_time DESC
""", engine)

st.dataframe(df, use_container_width=True)
