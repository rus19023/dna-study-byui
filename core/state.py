# core/state.py
import streamlit as st
import random


def init_auth_state():
    """Initialize authentication state if not present"""
    if "username" not in st.session_state:
        st.session_state.username = None


def set_user(username):
    """Set the logged-in user"""
    st.session_state.username = username


def get_current_user():
    """Get the currently logged-in username or None"""
    return st.session_state.get("username")


def logout_user():
    """Clear user authentication"""
    if "username" in st.session_state:
        del st.session_state.username


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
        st.session_state.show_answer = False
        st.session_state.current_deck = deck_name


def reset_study_state():
    """Clear all study-related session state"""
    keys_to_clear = ["cards", "index", "show_answer", "current_deck"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def reset_all_state():
    """Clear ALL session state (useful for complete logout/reset)"""
    st.session_state.clear()