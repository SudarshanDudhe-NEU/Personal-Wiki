import streamlit as st
from personal_wiki.app.utils.file import get_md_files
from personal_wiki.app.ui.sidebar import create_sidebar_navigation
from personal_wiki.app.ui.content import handle_file_selection, display_content
from personal_wiki.app.ui.css import local_css

# Set page configuration
st.set_page_config(
    page_title="Personal Wiki Viewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    """Main application entrypoint"""
    # Initialize UI
    local_css()

    # Get wiki structure
    md_files = get_md_files()

    # Set up navigation
    create_sidebar_navigation(md_files)

    # Handle file selection
    selected_file_path = handle_file_selection()

    # Display content
    display_content(selected_file_path)

if __name__ == "__main__":
    main()
