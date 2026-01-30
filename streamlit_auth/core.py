# streamlit_auth/core.py
"""Core authentication logic and session management"""
import streamlit as st
from typing import Optional, Callable
from functools import wraps


# Import from the auth module's database, NOT data/db.py
from .database import AuthDatabase  # ← Make sure this is here
from .config import AuthConfig


# Global database instance
_auth_db = None


def get_auth_db(config=None):
    """Get or create auth database instance"""
    global _auth_db
    
    if _auth_db is None:
        if config is None:
            config = AuthConfig.from_secrets()
        _auth_db = AuthDatabase(config)
    
    return _auth_db


def init_auth(config=None):
    """Initialize authentication system"""
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    
    # Initialize database
    get_auth_db(config)


def login_user(username: str, password: str) -> bool:
    """Login user with credentials"""
    db = get_auth_db()
    user = db.authenticate(username, password)
    
    if user:
        st.session_state.username = username
        st.session_state.user_data = user
        return True
    
    return False


def logout_user():
    """Logout current user"""
    if "username" in st.session_state:
        del st.session_state.username
    if "user_data" in st.session_state:
        del st.session_state.user_data


def get_current_user() -> Optional[str]:
    """Get currently logged-in username"""
    return st.session_state.get("username")


def get_user_data() -> Optional[dict]:
    """Get current user's data"""
    return st.session_state.get("user_data")


def is_admin() -> bool:
    """Check if current user is admin"""
    user_data = get_user_data()
    return user_data.get("is_admin", False) if user_data else False


def require_auth(func: Callable) -> Callable:
    """Decorator: Require authentication to access function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            st.warning("⚠️ Please login to access this feature")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func: Callable) -> Callable:
    """Decorator: Require admin privileges"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_admin():
            st.error("🚫 Admin access required")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
