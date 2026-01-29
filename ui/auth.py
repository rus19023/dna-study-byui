# ui/auth.py

import streamlit as st
from data.user_store import get_user, create_user
from core.state import init_auth_state, set_user, get_current_user, logout_user


def handle_authentication():
    """
    Handle login/register in sidebar and return logged-in username or None
    """
    # Initialize auth state
    init_auth_state()
    
    # Check if user is already logged in
    current_user = get_current_user()
    if current_user:
        return current_user
    
    st.sidebar.title("🧬 DNA Study")
    
    # Login/Register toggle
    auth_mode = st.sidebar.radio("", ["Login", "Register"])

    if auth_mode == "Login":
        username = st.sidebar.text_input(
            "Username",
            key="login_username"
        )
        password = st.sidebar.text_input(
            "Password", 
            type="password",
            key="login_password"
        )
        
        if st.sidebar.button(
            "Login", 
            type="primary", 
            use_container_width=True
        ):
            if username.strip() and password.strip():
                user = get_user(username.strip())
                if user and user.get("password") == password:
                    # Use state management function
                    set_user(username.strip())
                    st.rerun()
                else:
                    st.sidebar.error("Invalid username or password")
            else:
                st.sidebar.error("Please enter username and password")

    else:  # Register
        new_username = st.sidebar.text_input(
            "Choose Username", 
            key="reg_username"
        )
        new_password = st.sidebar.text_input(
            "Choose Password", 
            type="password", 
            key="reg_password"
        )
        confirm_password = st.sidebar.text_input(
            "Confirm Password", 
            type="password", 
            key="reg_confirm"
        )
        
        if st.sidebar.button(
            "Register",
            type="primary",
            use_container_width=True
        ):
            if new_username.strip() and new_password.strip():
                if new_password != confirm_password:
                    st.sidebar.error("Passwords don't match")
                elif get_user(new_username.strip()):
                    st.sidebar.error("Username already exists")
                else:
                    create_user(new_username.strip(), new_password)
                    st.sidebar.success(
                        f"User '{new_username}' created! Please login."
                    )
            else:
                st.sidebar.error("Please fill all fields")
 
    return None


def show_user_sidebar(username):
    """Show logged-in user info and logout button"""
    st.sidebar.write(f"👤 **{username}**")
  
    if st.sidebar.button(
        "🚪 Logout", 
        use_container_width=True,
        type="secondary"
    ):
        # Use state management function
        logout_user()
        st.rerun()