import streamlit as st
from auth import authenticate

st.set_page_config(page_title="Ecommerce Platform", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🔐 Login")

if not st.session_state.logged_in:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = int(user.user_id)
            st.session_state.username = user.username
            st.session_state.role = user.role
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

else:
    st.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

    if st.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
