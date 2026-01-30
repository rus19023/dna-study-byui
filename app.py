import streamlit as st

st.set_page_config(
    page_title="Flashcard Study",
    page_icon="🧬",
    layout="wide"
)

from streamlit_auth import (
    init_auth,
    render_sidebar_auth,
    render_admin_panel,
    get_current_user,
    get_user_data
)

# Your existing imports
from core.state import init_study_state
from ui.components import leaderboard, mode_selector
from ui.study_tab import render_study_tab
from ui.stats_tab import render_stats_tab
from ui.add_card_tab import render_add_card_tab
from ui.manage_tab import render_manage_tab
from data.deck_store import get_deck_names, get_deck
from data.user_store import get_leaderboard


# ----------------------------
# Initialize Authentication
# ----------------------------
init_auth()

# Handle authentication in sidebar
logged_in_user = render_sidebar_auth()

if not logged_in_user:
    st.title("🧬 Flashcard Study App")
    st.info("Please login or register in the sidebar to continue.")
    st.stop()

# User is logged in
st.sidebar.divider()

# Study mode selector
study_mode = mode_selector()
st.sidebar.divider()

# Deck selection
deck_names = get_deck_names()
if not deck_names:
    st.error("No decks found in database.")
    st.stop()

deck_name = st.sidebar.selectbox("Choose a deck", options=deck_names)
st.sidebar.divider()


# ----------------------------
# Main Page
# ----------------------------
st.title("🧬 Flashcard Study App")

# Get user data from auth module
user_data = get_user_data()
if not user_data:
    st.error("User not found")
    st.stop()

st.divider()

# Track deck changes
if "current_deck" not in st.session_state or st.session_state.current_deck != deck_name:
    st.session_state.current_deck = deck_name
    if "cards" in st.session_state:
        del st.session_state.cards

cards = get_deck(deck_name)


# app.py - Update the Tabs section

# ----------------------------
# Tabs
# ----------------------------
# Base tabs for all users
tabs = ["📚 Study", "📊 Stats", "🏆 Leaderboard"]

# Add admin-only tabs
if user_data.get("is_admin", False):
    tabs.extend(["➕ Add Card", "🗂️ Manage Decks", "🛡️ Admin"])

tab_objects = st.tabs(tabs)

# Tab 1: Study (always available)
with tab_objects[0]:
    render_study_tab(cards, deck_name, logged_in_user, study_mode, init_study_state)

# Tab 2: Stats (always available)
with tab_objects[1]:
    render_stats_tab(user_data)

# Tab 3: Leaderboard (always available)
with tab_objects[2]:
    top_users = get_leaderboard(limit=10)
    leaderboard(top_users)

# Admin-only tabs
if user_data.get("is_admin", False):
    # Tab 4: Add Card (admin only)
    with tab_objects[3]:
        render_add_card_tab()
    
    # Tab 5: Manage Decks (admin only)
    with tab_objects[4]:
        render_manage_tab()
    
    # Tab 6: Admin Panel (admin only)
    with tab_objects[5]:
        render_admin_panel()