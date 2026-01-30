# test_import.py
import sys
print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying to import...")
try:
    import streamlit_auth
    print(f"✅ Success! Module location: {streamlit_auth.__file__}")
    print(f"Available: {dir(streamlit_auth)}")
except ImportError as e:
    print(f"❌ Failed: {e}")