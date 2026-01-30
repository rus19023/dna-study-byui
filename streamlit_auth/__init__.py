# streamlit_auth/__init__.py
"""
Streamlit Authentication & Admin Module
A reusable authentication system for Streamlit apps
"""

from .core import (
    init_auth,
    login_user,
    logout_user,
    get_current_user,
    get_user_data,
    is_admin,
    require_auth,
    require_admin
)

from .ui import (
    render_login_page,
    render_sidebar_auth,
    render_user_info
)

from .admin import (
    render_admin_panel
)

from .config import AuthConfig

__version__ = "1.0.0"
__all__ = [
    "init_auth",
    "login_user", 
    "logout_user",
    "get_current_user",
    "get_user_data",
    "is_admin",
    "require_auth",
    "require_admin",
    "render_login_page",
    "render_sidebar_auth",
    "render_user_info",
    "render_admin_panel",
    "AuthConfig"
]