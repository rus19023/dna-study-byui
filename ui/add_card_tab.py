# ui/add_card_tab.py (update the render_add_card_tab function)

import streamlit as st
import base64
from data.deck_store import add_card_to_deck, get_deck_names

def render_add_card_tab():
    st.subheader("➕ Add New Card")
    
    deck_names = get_deck_names()
    if not deck_names:
        st.warning("No decks available. Create a deck first.")
        return
    
    selected_deck = st.selectbox("Select deck", deck_names)
    
    with st.form("add_card_form"):
        question = st.text_area("Question", height=100)
        answer = st.text_area("Answer", height=150)
        
        # Image upload
        st.markdown("**Optional: Add image to answer**")
        uploaded_file = st.file_uploader(
            "Upload image (appears with answer)",
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Image will be shown when the answer is revealed"
        )
        
        submitted = st.form_submit_button("💾 Add Card", type="primary")
        
        if submitted:
            if question.strip() and answer.strip():
                # Convert image to base64 if uploaded
                image_data = None
                if uploaded_file:
                    bytes_data = uploaded_file.read()
                    image_data = base64.b64encode(bytes_data).decode()
                
                if add_card_to_deck(selected_deck, question, answer, image_data):
                    st.success("✅ Card added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add card")
            else:
                st.warning("Please fill in both question and answer")
                
                