import streamlit as st
import pandas as pd
from db import get_engine

# Security block
if not st.session_state.get("logged_in") or st.session_state.get("role") != "stakeholder":
    st.error("🚫 Access Denied")
    st.stop()

engine = get_engine()

st.title("📊 RFM Dashboard")

query = """
SELECT 
    c.customer_id,
    DATEDIFF(CURDATE(), MAX(o.order_date)) AS recency,
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(oi.quantity * oi.price) AS monetary
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id
"""

rfm = pd.read_sql(query, engine)

st.metric("Total Revenue", f"${rfm['monetary'].sum():,.2f}")
st.bar_chart(rfm["monetary"])
st.dataframe(rfm)
