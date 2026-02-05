# core/state.py
import streamlit as st
import random
import secrets


def init_auth_state():
    """Initialize authentication state if not present"""
    if "username" not in st.session_state:
        st.session_state.username = None


def set_user(username):
    """Set the logged-in user with a session token"""
    # Generate a random session token
    token = secrets.token_urlsafe(32)
    st.session_state.username = username
    st.session_state.session_token = token
    
    # Store token in query params for persistence
    st.query_params["session"] = token
    
    # Store mapping in session state (in production, use database)
    if "session_tokens" not in st.session_state:
        st.session_state.session_tokens = {}
    st.session_state.session_tokens[token] = username


def get_current_user():
    """Get the currently logged-in username or None"""
    # First check session state
    if st.session_state.get("username"):
        return st.session_state.username
    
    # Check if there's a session token in query params
    if "session" in st.query_params:
        token = st.query_params["session"]
        if "session_tokens" not in st.session_state:
            st.session_state.session_tokens = {}
        
        # Check if token is valid
        if token in st.session_state.session_tokens:
            username = st.session_state.session_tokens[token]
            st.session_state.username = username
            return username
    
    return None


def logout_user():
    """Clear user authentication"""
    # Remove token from mapping
    if st.session_state.get("session_token"):
        token = st.session_state.session_token
        if "session_tokens" in st.session_state and token in st.session_state.session_tokens:
            del st.session_state.session_tokens[token]
    
    # Clear session state
    if "username" in st.session_state:
        del st.session_state.username
    if "session_token" in st.session_state:
        del st.session_state.session_token
    
    # Clear query params
    st.query_params.clear()


def init_study_state(cards, deck_name=None):
    """
    Initialize or reset the study session state.
    
    Args:
        cards: List of flashcards
        deck_name: Unique identifier for the current deck (e.g., deck name)
    """
    # Check if we need to initialize or if deck has changed
    current_deck = st.session_state.get("current_deck")
    
    if "cards" not in st.session_state or current_deck != deck_name:
        # Initialize/reset state
        st.session_state.cards = list(cards)
        random.shuffle(st.session_state.cards)
        st.session_state.index = 0
        st.session_state.current_deck = deck_name
    
    # Always initialize these if they don't exist (but don't reset if they do)
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "index" not in st.session_state:
        st.session_state.index = 0


def reset_study_state():
    """Clear all study-related session state"""
    keys_to_clear = ["cards", "index", "show_answer", "current_deck"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def reset_all_state():
    """Clear ALL session state (useful for complete logout/reset)"""
    st.session_state.clear()
    