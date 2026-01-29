# data/db.py
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import certifi

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
        
        # Use certifi for SSL certificates
        _client = MongoClient(
            mongo_uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
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