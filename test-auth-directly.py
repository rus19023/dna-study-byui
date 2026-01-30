# test_auth_directly.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force reload
import importlib
if 'streamlit_auth.database' in sys.modules:
    del sys.modules['streamlit_auth.database']
if 'streamlit_auth' in sys.modules:
    del sys.modules['streamlit_auth']

from streamlit_auth.database import AuthDatabase

print("AuthDatabase class loaded")
print("\nMethods in AuthDatabase:")
methods = [m for m in dir(AuthDatabase) if not m.startswith('_')]
for m in methods:
    print(f"  - {m}")

print(f"\nHas 'authenticate'? {'authenticate' in methods}")

# Check the actual file being used
print(f"\nFile location: {AuthDatabase.__module__}")
import streamlit_auth