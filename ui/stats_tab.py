# ui/stats_tab.py

import streamlit as st
from ui.components import user_stats


def render_stats_tab(user_data):
    """Render the stats tab"""
    st.subheader("Your Statistics")
    user_stats(user_data)
    
    st.divider()
    st.write("### Additional Stats")
    
    total = user_data.get("cards_studied", 0)
    
    if total > 0:
        st.write(f"**Best Streak:** {user_data.get('best_streak', 0)} 🔥")
        st.write(f"**Total Cards Studied:** {total}")
        st.write(f"**Correct Answers:** {user_data.get('correct_answers', 0)}")
        st.write(f"**Incorrect Answers:** {user_data.get('incorrect_answers', 0)}")
        
        # Verification stats
        verif_passed = user_data.get("verification_passed", 0)
        verif_failed = user_data.get("verification_failed", 0)
        verif_total = verif_passed + verif_failed
        
        if verif_total > 0:
            verif_accuracy = (verif_passed / verif_total * 100)
            st.write(
                f"**Verification Accuracy:** {verif_accuracy:.1f}% "
                f"({verif_passed}/{verif_total})"
            )
    else:
        st.info("Start studying to see your stats!")