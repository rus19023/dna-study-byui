# data/db.py
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

_client = None
_db = None

def get_db():
    """Get MongoDB database connection with error handling"""
    global _client, _db
    
    if _db is not None:
        return _db
    
    try:
        # Get connection string from secrets
        mongo_uri = st.secrets["mongo"]["uri"]
        db_name = st.secrets["mongo"]["db_name"]
        
        # Add SSL/TLS parameters for Streamlit Cloud compatibility
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=False,  # Set to True only for debugging
        )
        
        # Test the connection
        _client.admin.command('ping')
        _db = _client[db_name]
        
        return _db
        
    except ServerSelectionTimeoutError as e:
        st.error("❌ Cannot connect to MongoDB. Please check your connection.")
        st.error(f"Error: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Database connection error: {str(e)}")
        st.stop()