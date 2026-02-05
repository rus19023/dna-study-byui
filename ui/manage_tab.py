# ui/manage_tab.py

import streamlit as st
from data.deck_store import (
    get_deck_names,
    get_all_cards_with_indices,
    delete_card,
    edit_card,
    find_duplicate_cards,
    delete_deck,
    rename_deck,
    create_deck
)

def render_manage_tab():
    st.header("🗂️ Manage Decks")
    
    # Create two columns for deck management and card management
    deck_col, card_col = st.columns([1, 1])
    
    with deck_col:
        st.subheader("Deck Operations")
        
        # Get all decks
        deck_names = get_deck_names()
        
        if not deck_names:
            st.warning("No decks available")
            return
        
        # Deck selector for management
        selected_deck = st.selectbox(
            "Select deck to manage",
            options=deck_names,
            key="manage_deck_selector"
        )
        
        st.divider()
        
        # Create new deck
        with st.expander("➕ Create New Deck"):
            new_deck_name = st.text_input("New deck name", key="new_deck_name")
            if st.button("Create Deck", key="create_deck_btn"):
                if new_deck_name.strip():
                    if create_deck(new_deck_name.strip()):
                        st.success(f"✅ Created deck: {new_deck_name}")
                        st.rerun()
                    else:
                        st.error("❌ Deck already exists or creation failed")
                else:
                    st.warning("Please enter a deck name")
        
        # Rename deck
        with st.expander("✏️ Rename Deck"):
            new_name = st.text_input(
                f"Rename '{selected_deck}' to:",
                key="rename_deck_input"
            )
            if st.button("Rename Deck", key="rename_deck_btn"):
                if new_name.strip() and new_name != selected_deck:
                    if rename_deck(selected_deck, new_name.strip()):
                        st.success(f"✅ Renamed '{selected_deck}' to '{new_name}'")
                        st.rerun()
                    else:
                        st.error("❌ New name already exists or rename failed")
                else:
                    st.warning("Please enter a different name")
        
        # Delete deck
        with st.expander("🗑️ Delete Deck", expanded=False):
            st.warning(f"⚠️ This will permanently delete '{selected_deck}' and all its cards!")
            confirm_delete = st.text_input(
                f"Type '{selected_deck}' to confirm deletion:",
                key="confirm_delete_deck"
            )
            if st.button("Delete Deck", type="primary", key="delete_deck_btn"):
                if confirm_delete == selected_deck:
                    if delete_deck(selected_deck):
                        st.success(f"✅ Deleted deck: {selected_deck}")
                        st.rerun()
                    else:
                        st.error("❌ Deletion failed")
                else:
                    st.error("❌ Confirmation text doesn't match")
    
    with card_col:
        st.subheader(f"Card Management: {selected_deck}")
        
        # Get all cards for the selected deck
        cards = get_all_cards_with_indices(selected_deck)
        
        if not cards:
            st.info("No cards in this deck")
            return
        
        st.write(f"**Total cards:** {len(cards)}")
        
        # Find duplicates
        duplicates = find_duplicate_cards(selected_deck)
        if duplicates:
            st.warning(f"⚠️ Found {len(duplicates)} duplicate question(s)")
            with st.expander("View Duplicates"):
                for dup in duplicates:
                    st.write(f"**Index {dup['index']}** (duplicate of index {dup['original_index']}):")
                    st.write(f"Q: {dup['question']}")
                    st.write(f"A: {dup['answer']}")
                    if st.button(f"Delete duplicate #{dup['index']}", key=f"del_dup_{dup['index']}"):
                        if delete_card(selected_deck, dup['index']):
                            st.success(f"Deleted card #{dup['index']}")
                            st.rerun()
                    st.divider()
        
        st.divider()
        
        # Card operations
        tab1, tab2 = st.tabs(["📝 Edit Cards", "🗑️ Delete Cards"])
        
        with tab1:
            st.subheader("Edit Card")
            
            # Select card to edit
            card_options = [f"#{c['index']}: {c['question'][:50]}..." for c in cards]
            selected_card_str = st.selectbox(
                "Select card to edit",
                options=card_options,
                key="edit_card_selector"
            )
            
            if selected_card_str:
                # Extract index
                card_index = int(selected_card_str.split(":")[0].replace("#", ""))
                
                # Find the actual card with this index (don't use list position!)
                card = next((c for c in cards if c['index'] == card_index), None)
                
                if card:
                    st.write(f"**Editing card #{card_index}**")
                    
                    # Edit form
                    with st.form(key=f"edit_form_{card_index}"):
                        new_question = st.text_area(
                            "Question",
                            value=card['question'],
                            height=100,
                            key=f"edit_q_{card_index}"
                        )
                        new_answer = st.text_area(
                            "Answer",
                            value=card['answer'],
                            height=150,
                            key=f"edit_a_{card_index}"
                        )
                        
                        submitted = st.form_submit_button("💾 Save Changes", type="primary")
                        
                        if submitted:
                            if new_question.strip() and new_answer.strip():
                                if edit_card(selected_deck, card_index, new_question, new_answer):
                                    st.success(f"✅ Updated card #{card_index}")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update card")
                            else:
                                st.warning("Question and answer cannot be empty")
                        
        with tab2:
            st.subheader("Delete Card")
            
            # Select card to delete
            delete_card_options = [f"#{c['index']}: {c['question'][:50]}..." for c in cards]
            selected_delete_str = st.selectbox(
                "Select card to delete",
                options=delete_card_options,
                key="delete_card_selector"
            )
            
            if selected_delete_str:
                # Extract index
                delete_index = int(selected_delete_str.split(":")[0].replace("#", ""))
                delete_card_data = cards[delete_index]
                
                st.write(f"**Card #{delete_index}**")
                st.info(f"**Q:** {delete_card_data['question']}")
                st.info(f"**A:** {delete_card_data['answer']}")
                
                if st.button(
                    f"🗑️ Delete Card #{delete_index}",
                    type="primary",
                    key=f"confirm_delete_{delete_index}"
                ):
                    if delete_card(selected_deck, delete_index):
                        st.success(f"✅ Deleted card #{delete_index}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete card")
