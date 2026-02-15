import streamlit as st
import pandas as pd
from db import get_engine

# 🔐 Security block
if not st.session_state.get("logged_in") or st.session_state.get("role") != "stakeholder":
    st.error("🚫 Access Denied")
    st.stop()

engine = get_engine()

st.title("📊 RFM Dashboard")

# PostgreSQL-compatible RFM query
query = """
SELECT 
    c.customer_id,
    (CURRENT_DATE - MAX(o.order_date))::int AS recency_days,  -- days since last order
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(oi.quantity * oi.price) AS monetary
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id
ORDER BY monetary DESC
"""

# Fetch data
rfm = pd.read_sql(query, engine)

# Display metrics
st.metric("Total Revenue", f"${rfm['monetary'].sum():,.2f}")

# Visualizations
st.subheader("Revenue by Customer")
st.bar_chart(rfm.set_index("customer_id")["monetary"])

st.subheader("RFM Table")
st.dataframe(rfm)
