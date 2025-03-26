import streamlit as st
from personal_wiki.app.utils.file import get_md_files
from personal_wiki.app.utils.markdown import md_to_html, process_images, process_links
import os
import re

def create_sidebar_navigation(md_files):
    """Create the sidebar navigation from the wiki structure with enhanced design"""
    # Apply custom CSS for sidebar enhancements
    from personal_wiki.app.ui.css import apply_sidebar_css
    apply_sidebar_css()
    
    # Header section with logo and title
    with st.sidebar.container():
        col1, col2 = st.sidebar.columns([1, 3])
        with col1:
            st.markdown("📚")  # Book emoji as logo
        with col2:
            st.markdown("### Personal Wiki")

    st.sidebar.divider()
    
    # Add theme selector to the sidebar
    from personal_wiki.app.ui.theme import show_theme_selector
    show_theme_selector()
    
    # Search box for filtering content
    search_term = st.sidebar.text_input("🔍 Search wiki", key="search_wiki")
    if search_term:
        from personal_wiki.app.utils.search import search_wiki_content
        search_results = search_wiki_content(search_term, md_files)
        if search_results:
            st.sidebar.markdown("### Search Results")
            for result in search_results:
                if st.sidebar.button(f"📝 {result['title']}", key=f"search_{result['path']}"):
                    st.session_state.selected_file = result['path']
                    st.experimental_set_query_params(file=result['path'])
                    st.rerun()
    
    # Home/index button
    if st.sidebar.button("📄 Home", key="home_button", use_container_width=True):
        st.session_state.selected_file = "index.md"
        st.experimental_set_query_params(file="index.md")
        st.rerun()
    
    # Categories in sidebar with active state highlighting
    current_file = st.session_state.get("selected_file", "")
    from personal_wiki.app.utils.file import get_category_from_path
    current_category = get_category_from_path(current_file)
    
    for category_name, category_data in md_files.items():
        is_active = category_name == current_category
        render_category_section(category_name, category_data, is_active)


def render_category_section(category_name, category_data, is_active=False):
    """Render a category section in the sidebar with enhanced styling"""
    category_title = category_name.capitalize()
    active_class = "active-category" if is_active else "category-item"

    # Category expander with active state highlighting
    with st.sidebar.expander(f"📁 {category_title}", expanded=is_active):
        # Category main page button
        if st.button(
            f"📄 Overview",
            key=f"cat_{category_name}",
            help=f"View {category_title} overview",
            use_container_width=True,
        ):
            st.session_state.selected_file = category_data["path"]
            st.experimental_set_query_params(file=category_data["path"])
            st.rerun()

        # Files directly in the category
        if "files" in category_data and category_data["files"]:
            render_file_list(category_name, category_data["files"])
        else:
            st.markdown(
                "<div class='sidebar-note'>No files in this category</div>",
                unsafe_allow_html=True,
            )

        # Subcategories if they exist
        if "subcategories" in category_data and category_data["subcategories"]:
            render_subcategories(category_name, category_data["subcategories"])


def render_file_list(category_name, files):
    """Render a list of files with enhanced styling"""
    # Get current file to highlight active item
    current_file = st.session_state.get("selected_file", "")

    for file_name, file_path in files.items():
        # Check if this file is the active one
        is_active = file_path == current_file
        active_class = "active-file" if is_active else ""
        title_display = file_name.replace("-", " ").title()
        
        # Use a button instead of JavaScript onclick
        if st.button(f"📝 {title_display}", 
                  key=f"file_{category_name}_{file_name}", 
                  use_container_width=True,
                  type="secondary" if is_active else "primary"):
            st.session_state.selected_file = file_path
            st.experimental_set_query_params(file=file_path)
            st.rerun()


def render_subcategories(category_name, subcategories):
    """Render subcategories within a category with enhanced styling"""
    st.markdown("#### Subcategories")

    for subcategory_name, subcategory_data in subcategories.items():
        subcat_display = subcategory_name.replace("-", " ").title()

        # Display subcategory as a section with proper formatting
        st.markdown(
            f"""
            <div class="subcategory-label">
                <span>📁 {subcat_display}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Subcategory index if it exists
        if "index" in subcategory_data:
            if st.button(f"📄 {subcat_display} Index", 
                      key=f"subcat_idx_{category_name}_{subcategory_name}",
                      use_container_width=True):
                st.session_state.selected_file = subcategory_data["index"]
                st.experimental_set_query_params(file=subcategory_data["index"])
                st.rerun()

        # Files in the subcategory
        render_subcategory_files(category_name, subcategory_name, subcategory_data)


def render_subcategory_files(category_name, subcategory_name, subcategory_data):
    """Render files within a subcategory with enhanced styling"""
    current_file = st.session_state.get("selected_file", "")

    for subfile_name, subfile_path in subcategory_data.get("files", {}).items():
        # Check if this file is the active one
        is_active = subfile_path == current_file
        active_class = "active-file" if is_active else ""
        subtitle_display = subfile_name.replace("-", " ").title()
        
        # Use Streamlit buttons for better compatibility
        if st.button(f"📝 {subtitle_display}", 
                  key=f"subfile_{category_name}_{subcategory_name}_{subfile_name}",
                  use_container_width=True,
                  type="secondary" if is_active else "primary"):
            st.session_state.selected_file = subfile_path
            st.experimental_set_query_params(file=subfile_path)
            st.rerun()


def handle_markdown_display(md_content, selected_file_path):
    """Process and display markdown content with proper code block handling"""
    # Convert to HTML first
    html_content = md_to_html(md_content)
    
    # Process images and links
    html_content = process_images(html_content, selected_file_path)
    html_content = process_links(html_content, selected_file_path)
    
    # Final rendering
    st.markdown(html_content, unsafe_allow_html=True)