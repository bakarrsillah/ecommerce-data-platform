import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import get_engine

# 🔐 Security Check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "clerk":
    st.error("🚫 Access Denied")
    st.stop()

engine = get_engine()

st.title("🧾 Sales Entry")

customers = pd.read_sql(
    "SELECT customer_id, CONCAT(first_name,' ',last_name) AS name FROM customers",
    engine
)

products = pd.read_sql(
    "SELECT product_id, product_name, price FROM products",
    engine
)

customer = st.selectbox("Customer", customers["name"])
product = st.selectbox("Product", products["product_name"])
quantity = st.number_input("Quantity", min_value=1, value=1)

if st.button("Submit Sale"):

    # Convert safely to Python native types
    customer_id = int(customers.loc[customers["name"] == customer, "customer_id"].values[0])

    product_row = products.loc[products["product_name"] == product]
    product_id = int(product_row["product_id"].values[0])
    price = float(product_row["price"].values[0])
    quantity = int(quantity)

    total_amount = float(quantity * price)

    try:
        with engine.begin() as conn:

            # 1️⃣ Insert Order
            result = conn.execute(
                text("""
                    INSERT INTO orders (customer_id, order_date, status)
                    VALUES (:cid, NOW(), 'Completed')
                """),
                {"cid": customer_id}
            )

            order_id = int(result.lastrowid)

            # 2️⃣ Insert Order Item
            conn.execute(
                text("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (:oid, :pid, :qty, :price)
                """),
                {
                    "oid": order_id,
                    "pid": product_id,
                    "qty": quantity,
                    "price": price
                }
            )

            # 3️⃣ Insert Payment
            conn.execute(
                text("""
                    INSERT INTO payments (order_id, amount, payment_method)
                    VALUES (:oid, :amount, 'Cash')
                """),
                {
                    "oid": order_id,
                    "amount": total_amount
                }
            )

            # 4️⃣ Insert Audit Log
            conn.execute(
                text("""
                    INSERT INTO audit_log 
                    (user_id, username, action_type, table_name, record_id, details)
                    VALUES (:uid, :uname, :action, :table, :rid, :details)
                """),
                {
                    "uid": int(st.session_state["user_id"]),
                    "uname": st.session_state["username"],
                    "action": "INSERT_ORDER",
                    "table": "orders",
                    "rid": order_id,
                    "details": f"CustomerID={customer_id}, ProductID={product_id}, Total={total_amount}"
                }
            )

        st.success(f"✅ Sale recorded! Total: ${total_amount:.2f}")

    except Exception as e:
        st.error(f"Error: {e}")
