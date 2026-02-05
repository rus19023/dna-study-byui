# streamlit_auth/admin.py
"""Admin panel UI components"""
import streamlit as st
from typing import Optional


def render_admin_panel(config=None):
    """Render admin control panel"""
    from .core import get_auth_db, require_admin, is_admin
    from .config import AuthConfig
    
    # Check admin access
    if not is_admin():
        st.error("🚫 Admin access required")
        st.stop()
    
    if config is None:
        config = AuthConfig.from_secrets()
    
    st.subheader("🛡️ Admin Panel")
    
    db = get_auth_db(config)
    
    # User management
    st.markdown("### 👥 User Management")
    
    all_users = db.get_all_users()
    
    if not all_users:
        st.info("No users in system")
        return
    
    # User table
    user_data = []
    for user in all_users:
        user_data.append({
            "Username": user["_id"],
            "Admin": "✅" if user.get("is_admin") else "❌",
            "Score": user.get("total_score", 0),
            "Active": "✅" if user.get("is_active", True) else "❌"
        })
    
    st.dataframe(user_data, width="stretch")
    
    st.divider()
    
    # User actions
    st.markdown("### ⚙️ User Actions")
    
    selected_user = st.selectbox(
        "Select user:",
        options=[u["_id"] for u in all_users]
    )
    
    if selected_user:
        user = db.get_user(selected_user)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if user.get("is_admin"):
                if st.button("Remove Admin", width="stretch"):
                    db.remove_admin(selected_user)
                    st.success(f"Removed admin from {selected_user}")
                    st.rerun()
            else:
                if st.button("Make Admin", width="stretch"):
                    db.make_admin(selected_user)
                    st.success(f"Made {selected_user} an admin")
                    st.rerun()
        
        with col2:
            if st.button("Reset Score", width="stretch"):
                db.update_user(selected_user, {"total_score": 0})
                st.success(f"Reset score for {selected_user}")
                st.rerun()
        
        with col3:
            if st.button("Delete User", type="secondary", width="stretch"):
                if st.session_state.get("confirm_delete") == selected_user:
                    db.delete_user(selected_user)
                    st.success(f"Deleted {selected_user}")
                    st.session_state.confirm_delete = None
                    st.rerun()
                else:
                    st.session_state.confirm_delete = selected_user
                    st.warning("Click again to confirm deletion")
