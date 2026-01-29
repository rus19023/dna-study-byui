import streamlit as st

# try:
#     st.set_page_config(
#         page_title="Debug Test",
#         page_icon="🧬",
#     )
    
#     st.title("Test 1: Streamlit works!")
#     st.write("If you see this, basic Streamlit is working.")
    
#     # Test MongoDB secrets
#     st.write("Test 2: Checking secrets...")
#     if "mongo" in st.secrets:
#         st.success("✓ MongoDB secrets found")
#         st.write(f"URI starts with: {st.secrets['mongo']['uri'][:20]}...")
#     else:
#         st.error("✗ MongoDB secrets missing!")
    
#     # Test MongoDB connection
#     st.write("Test 3: Connecting to MongoDB...")
#     from pymongo import MongoClient
#     client = MongoClient(st.secrets["mongo"]["uri"])
#     db = client[st.secrets["mongo"]["db_name"]]
#     count = db.users.count_documents({})
#     st.success(f"✓ MongoDB connected! Found {count} users")
    
# except Exception as e:
#     import traceback
#     st.error("CRASH ERROR:")
#     st.code(traceback.format_exc())
    


st.set_page_config(
    page_title="Flashcard Study",
    page_icon="🧬",
    layout="wide"
)

from core.state import init_state
from ui.auth import handle_authentication, show_user_sidebar
from ui.components import leaderboard, mode_selector
from ui.study_tab import render_study_tab
from ui.stats_tab import render_stats_tab
from ui.add_card_tab import render_add_card_tab
from ui.manage_tab import render_manage_tab
from ui.admin_tab import render_admin_tab
from data.deck_store import get_deck_names, get_deck
from data.user_store import get_user, get_leaderboard


# ----------------------------
# Authentication
# ----------------------------
logged_in_user = handle_authentication()

if not logged_in_user:
    st.title("🧬 Flashcard Study App")
    st.info("Please login or register in the sidebar to continue.")
    st.stop()

# Show user sidebar with logout button
show_user_sidebar(logged_in_user)
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

current_user = get_user(logged_in_user)
if not current_user:
    st.error("User not found")
    st.stop()

st.divider()

# Track deck changes
if "current_deck" not in st.session_state or st.session_state.current_deck != deck_name:
    st.session_state.current_deck = deck_name
    if "cards" in st.session_state:
        del st.session_state.cards

cards = get_deck(deck_name)


# ----------------------------
# Tabs
# ----------------------------
tabs = ["📚 Study", "📊 Stats", "🏆 Leaderboard", "➕ Add Card", "🗂️ Manage Decks"]
if current_user.get("is_admin", False):
    tabs.append("🛡️ Admin")

tab_objects = st.tabs(tabs)

# Tab 1: Study
with tab_objects[0]:
    render_study_tab(cards, deck_name, logged_in_user, study_mode, init_state)

# Tab 2: Stats
with tab_objects[1]:
    render_stats_tab(current_user)

# Tab 3: Leaderboard
with tab_objects[2]:
    top_users = get_leaderboard(limit=10)
    leaderboard(top_users)

# Tab 4: Add Card
with tab_objects[3]:
    render_add_card_tab()

# Tab 5: Manage Decks
with tab_objects[4]:
    render_manage_tab()

# Tab 6: Admin (if user is admin)
if current_user.get("is_admin", False):
    with tab_objects[5]:
        render_admin_tab()