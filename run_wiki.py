import sys
import os
import streamlit as st

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now we can import from our package
from personal_wiki.app.main import main

if __name__ == "__main__":
    main()