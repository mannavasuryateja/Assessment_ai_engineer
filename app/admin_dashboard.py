import streamlit as st
from db.database import get_all_bookings
import os


def check_admin_password():
    """Check if admin is authenticated"""
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    return st.session_state.admin_authenticated


def login_form():
    """Display login form for admin dashboard"""
    st.header("🔐 Admin Login")
    
    # Get password from environment variable or use default
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    
    with st.form("admin_login"):
        password = st.text_input("Enter Admin Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    
    st.info("💡 Tip: Set the ADMIN_PASSWORD environment variable to change the default password.")


def render_admin_dashboard():
    """Render admin dashboard with password protection"""
    
    # Check authentication
    if not check_admin_password():
        login_form()
        return
    
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.header("📊 Admin Dashboard")
    with col2:
        if st.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()

    bookings = get_all_bookings()

    if not bookings:
        st.info("No bookings yet.")
        return

    st.dataframe(bookings)
