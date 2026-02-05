# streamlit_auth/ui.py
"""UI components for authentication"""
import streamlit as st
from typing import Optional


def render_sidebar_auth(config=None):
    """Render login/register in sidebar, return username if logged in"""
    from .core import login_user, logout_user, get_current_user, get_user_data, get_auth_db
    from .config import AuthConfig
    
    current_user = get_current_user()
    
    if current_user:
        # Show user info
        user_data = get_user_data()
        st.sidebar.write(f"👤 **{current_user}**")
        if user_data.get("is_admin"):
            st.sidebar.caption("🛡️ Admin")
        
        if st.sidebar.button("🚪 Logout", width="stretch"):
            logout_user()
            st.rerun()
        
        return current_user
    
    # Show login/register
    if config is None:
        config = AuthConfig.from_secrets()
    
    st.sidebar.title(config.login_title)
    
    auth_mode = st.sidebar.radio(
        "Authentication Mode",
        ["Login", "Register"] if config.allow_registration else ["Login"],
        label_visibility="collapsed"
    )
    
    if auth_mode == "Login":
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", width="stretch", type="primary")
            
            if submit:
                if username.strip() and password.strip():
                    if login_user(username.strip(), password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.error("Please enter username and password")
    
    elif auth_mode == "Register":
        with st.sidebar.form("register_form"):
            username = st.text_input("Username")
            if config.require_email:
                email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register", width="stretch", type="primary")
            
            if submit:
                if not username.strip() or not password.strip():
                    st.error("Please fill all fields")
                elif password != confirm:
                    st.error("Passwords don't match")
                else:
                    db = get_auth_db()
                    if db.get_user(username.strip()):
                        st.error("Username already exists")
                    else:
                        email_val = email if config.require_email else None
                        if db.create_user(username.strip(), password, email_val):
                            st.success("✅ Account created! Please login.")
                        else:
                            st.error("Failed to create account")
    
    return None


def render_login_page(config=None):
    """Render full-page login (alternative to sidebar)"""
    from .core import login_user, get_auth_db
    from .config import AuthConfig
    
    if config is None:
        config = AuthConfig.from_secrets()
    
    st.title(config.app_name)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader(config.login_title)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", width="stretch", type="primary")
                
                if submit:
                    if username.strip() and password.strip():
                        if login_user(username.strip(), password):
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
        
        with tab2:
            if config.allow_registration:
                with st.form("register_form"):
                    username = st.text_input("Username", key="reg_user")
                    if config.require_email:
                        email = st.text_input("Email")
                    password = st.text_input("Password", type="password", key="reg_pass")
                    confirm = st.text_input("Confirm Password", type="password")
                    submit = st.form_submit_button("Register", width="stretch", type="primary")
                    
                    if submit:
                        if password != confirm:
                            st.error("Passwords don't match")
                        else:
                            db = get_auth_db()
                            email_val = email if config.require_email else None
                            if db.create_user(username.strip(), password, email_val):
                                st.success("✅ Account created! Please login.")
                            else:
                                st.error("Failed to create account")
            else:
                st.info("Registration is disabled. Contact administrator.")


def render_user_info():
    """Render current user information"""
    from .core import get_user_data
    
    user_data = get_user_data()
    
    if not user_data:
        st.warning("Not logged in")
        return
    
    st.subheader("👤 User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Username", user_data["_id"])
        st.metric("Role", "Admin" if user_data.get("is_admin") else "User")
    
    with col2:
        if "email" in user_data and user_data["email"]:
            st.metric("Email", user_data["email"])
        st.metric("Total Score", user_data.get("total_score", 0))
