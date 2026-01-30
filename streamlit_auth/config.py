# streamlit_auth/config.py
"""Configuration for auth module"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthConfig:
    """Authentication configuration"""
    
    # MongoDB settings
    mongo_uri: str
    db_name: str
    
    # Collection names
    users_collection: str = "users"
    sessions_collection: str = "sessions"
    
    # App settings
    app_name: str = "Streamlit App"
    login_title: str = "🔐 Login"
    require_email: bool = False
    allow_registration: bool = True
    
    # Session settings
    session_expiry_days: int = 7
    
    @classmethod
    def from_secrets(cls, secrets_key: str = "mongo"):
        """Create config from Streamlit secrets"""
        import streamlit as st
        return cls(
            mongo_uri=st.secrets[secrets_key]["uri"],
            db_name=st.secrets[secrets_key]["db_name"],
            app_name=st.secrets.get("app", {}).get("name", "Streamlit App")
        )
