import streamlit as st
import pandas as pd
from db import get_engine

# 🔐 Security: Only stakeholders can access
if not st.session_state.get("logged_in") or st.session_state.get("role") != "stakeholder":
    st.error("🚫 Access Denied")
    st.stop()

engine = get_engine()

st.title("📊 RFM Dashboard")

# -----------------------------
# RFM Query for PostgreSQL
# -----------------------------
query = """
SELECT 
    c.customer_id,
    EXTRACT(DAY FROM (CURRENT_DATE - MAX(o.order_date))) AS recency_days,  -- days since last order
    COUNT(DISTINCT o.order_id) AS frequency,                               -- number of orders
    SUM(oi.quantity * oi.price) AS monetary                                 -- total spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id
ORDER BY monetary DESC
"""

# Execute query
rfm = pd.read_sql(query, engine)

# -----------------------------
# Metrics
# -----------------------------
total_revenue = rfm['monetary'].sum() if not rfm.empty else 0
st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")

# -----------------------------
# Charts
# -----------------------------
if not rfm.empty:
    st.subheader("Top Customers by Revenue")
    st.bar_chart(rfm.set_index('customer_id')['monetary'])

# -----------------------------
# Data Table
# -----------------------------
st.subheader("RFM Table")
st.dataframe(rfm)
