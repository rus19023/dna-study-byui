# streamlit_auth/database.py
"""Database operations for user management"""
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime
from typing import Optional, Dict, List
import certifi


class AuthDatabase:
    """Handle all database operations for authentication"""
    
    def __init__(self, config):
        self.config = config
        self._client = None
        self._db = None
    
    @property
    def db(self):
        """Get database connection"""
        if self._db is not None:
            return self._db
        
        try:
            import streamlit as st
            
            self._client = MongoClient(
                self.config.mongo_uri,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
            )
            
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[self.config.db_name]
            
            return self._db
            
        except ServerSelectionTimeoutError as e:
            import streamlit as st
            st.error("❌ Cannot connect to database")
            st.error(f"Error: {str(e)}")
            st.stop()
    
    # User operations
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        return self.db[self.config.users_collection].find_one({"_id": username})
    
    # streamlit_auth/database.py - Update the create_user method

    def create_user(self, username: str, password: str, 
                email: Optional[str] = None, is_admin: bool = False) -> bool:
        """Create new user"""
        try:
            user_doc = {
                "_id": username,
                "password": password,
                "email": email,
                "is_admin": is_admin,
                "created_at": datetime.utcnow(),
                "is_active": True,
                # Flashcard-specific fields
                "total_score": 0,
                "cards_studied": 0,
                "correct_answers": 0,
                "incorrect_answers": 0,
                "current_streak": 0,
                "best_streak": 0,
                "verification_passed": 0,
                "verification_failed": 0,
                "flagged": False
            }
            self.db[self.config.users_collection].insert_one(user_doc)
            return True
        except Exception as e:
            return False
        
        
    def update_user(self, username: str, updates: Dict) -> bool:
        """Update user fields"""
        try:
            self.db[self.config.users_collection].update_one(
                {"_id": username},
                {"$set": updates}
            )
            return True
        except:
            return False

    def delete_user(self, username: str) -> bool:
        """Delete user"""
        try:
            self.db[self.config.users_collection].delete_one({"_id": username})
            return True
        except:
            return False

    def get_all_users(self) -> List[Dict]:
        """Get all users (without passwords)"""
        return list(self.db[self.config.users_collection].find(
            {}, {"password": 0}
        ))

    def make_admin(self, username: str) -> bool:
        """Grant admin privileges"""
        return self.update_user(username, {"is_admin": True})

    def remove_admin(self, username: str) -> bool:
        """Remove admin privileges"""
        return self.update_user(username, {"is_admin": False})

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user credentials"""
        user = self.get_user(username)
        if user and user.get("password") == password and user.get("is_active", True):
            return user
        return None
