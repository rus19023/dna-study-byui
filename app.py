import streamlit as st

st.set_page_config(
    page_title="Flashcard Study",
    page_icon="🧬",
    layout="wide"
)


st.markdown("""
    <style>
    /* Text inputs and text areas */
    input[type="text"], 
    textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #4CAF50 !important;
        border-radius: 5px !important;
    }
    
    /* Selectboxes/Dropdowns */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        border: 2px solid #2196F3 !important;
        border-radius: 5px !important;
    }
    
    /* Hide the search input inside dropdowns or style it differently */
    [data-baseweb="select"] input {
        border: 1px solid #ccc !important;
        background-color: #f5f5f5 !important;
    }
    
    /* Buttons */
    .stButton > button {
        border: 2px solid #FF9800 !important;
        border-radius: 5px !important;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        border: 2px solid #9C27B0 !important;
        border-radius: 5px !important;
    }
    
    /* Forms */
    [data-testid="stForm"] {
        border: 3px solid #FF5722 !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)


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

# Study mode selector
study_mode = mode_selector()

# Deck selection
deck_names = get_deck_names()
if not deck_names:
    st.error("No decks found in database.")
    st.stop()

# Set your preferred default deck
default_deck = "Week 4 - Identity: DNA Profiling - Step 1"  # Change this to your deck name

# Find the index of the default deck, or use 0 if not found
default_index = deck_names.index(default_deck) if default_deck in deck_names else 0

deck_name = st.sidebar.selectbox(
    "Choose a deck", 
    options=deck_names,
    index=default_index  # This sets which deck shows first
)


# ----------------------------
# Main Page
# ----------------------------
st.title("🧬 Flashcard Study App")

# Get user data from auth module
user_data = get_user_data()
if not user_data:
    st.error("User not found")
    st.stop()

# Track deck changes
if "current_deck" not in st.session_state or st.session_state.current_deck != deck_name:
    st.session_state.current_deck = deck_name
    if "cards" in st.session_state:
        del st.session_state.cards

# Store cards in session state so callbacks can access them
st.session_state.cards = get_deck(deck_name)
cards = st.session_state.cards


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