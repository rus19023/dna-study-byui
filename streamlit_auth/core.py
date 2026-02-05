# streamlit_auth/core.py
"""Core authentication logic and session management"""
import streamlit as st
from typing import Optional, Callable
from functools import wraps
import hashlib
import time


# Import from the auth module's database, NOT data/db.py
from .database import AuthDatabase
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


def _create_session_token(username: str) -> str:
    """Create a simple session token"""
    timestamp = str(int(time.time()))
    return hashlib.sha256(f"{username}:{timestamp}".encode()).hexdigest()[:16]


def _persist_login(username: str):
    """Store login token in session state with timestamp"""
    token = _create_session_token(username)
    st.session_state['auth_token'] = token
    st.session_state['auth_username'] = username
    st.session_state['auth_timestamp'] = time.time()


def _check_persisted_login() -> Optional[str]:
    """Check if user has a valid persisted session"""
    if 'auth_token' in st.session_state and 'auth_username' in st.session_state:
        # Check if session is still valid (7 days)
        timestamp = st.session_state.get('auth_timestamp', 0)
        if time.time() - timestamp < (7 * 24 * 3600):  # 7 days
            return st.session_state['auth_username']
    return None


def init_auth(config=None):
    """Initialize authentication system"""
    # Check for persisted login first
    if "username" not in st.session_state:
        persisted_user = _check_persisted_login()
        if persisted_user:
            # Restore session from persisted login
            db = get_auth_db(config)
            user = db.get_user(persisted_user)
            if user and user.get("is_active", True):
                st.session_state.username = persisted_user
                st.session_state.user_data = user
            else:
                # Invalid session, clear it
                _clear_persisted_login()
    
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
        _persist_login(username)  # Persist the login
        return True
    
    return False


def _clear_persisted_login():
    """Clear persisted login data"""
    if 'auth_token' in st.session_state:
        del st.session_state.auth_token
    if 'auth_username' in st.session_state:
        del st.session_state.auth_username
    if 'auth_timestamp' in st.session_state:
        del st.session_state.auth_timestamp


def logout_user():
    """Logout current user"""
    if "username" in st.session_state:
        del st.session_state.username
    if "user_data" in st.session_state:
        del st.session_state.user_data
    _clear_persisted_login()


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