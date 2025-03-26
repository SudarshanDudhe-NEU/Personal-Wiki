import streamlit as st
import os
import datetime

from streamlit_utils import *
from streamlit_css_utils import *

# Set page configuration
st.set_page_config(
    page_title="Personal Wiki Viewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


def create_sidebar_navigation(md_files):
    """Create the sidebar navigation from the wiki structure with enhanced design"""
    # Apply custom CSS for sidebar enhancements
    apply_sidebar_css()

    # Header section with logo and title
    with st.sidebar.container():
        col1, col2 = st.sidebar.columns([1, 3])
        with col1:
            st.markdown("📚")  # Book emoji as logo
        with col2:
            st.markdown("### Personal Wiki")

    st.sidebar.divider()

    # Search box for filtering content
    search_term = st.sidebar.text_input("🔍 Search wiki", key="search_wiki")

    # Home/index button with hover effect
    home_container = st.sidebar.container()
    home_container.markdown(
        """
        <div class="nav-button home-button" onclick="homeClick()">
            <div class="nav-icon">📄</div>
            <div class="nav-label">Home</div>
        </div>
        <script>
            function homeClick() {
                window.location.search = '?file=index.md';
            }
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Detect active section based on current file
    current_file = st.session_state.get("selected_file", "")
    current_category = get_category_from_path(current_file)

    # Favorites section (pinned pages)
    with st.sidebar.expander("⭐ Favorites", expanded=False):
        st.markdown(
            """
            <div class="sidebar-note">Pin your favorite pages here</div>
            """,
            unsafe_allow_html=True,
        )
        # Placeholder for favorites - this would be populated from user settings

    st.sidebar.divider()

    # Categories in sidebar - enhanced with active state highlighting
    for category_name, category_data in md_files.items():
        is_active = category_name == current_category
        render_category_section(category_name, category_data, is_active)

    # Mobile responsiveness notice
    st.sidebar.markdown(
        "<div class='mobile-notice'>Swipe right for content →</div>",
        unsafe_allow_html=True,
    )

    # Footer with app info
    st.sidebar.divider()
    st.sidebar.markdown(
        "<div class='sidebar-footer'>Wiki Viewer v1.0</div>", unsafe_allow_html=True
    )


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
            st.query_params["file"] = category_data["path"]
            st.rerun()

        # Files directly in the category
        if category_data["files"]:
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

        # Create a container for the file item
        file_container = st.container()

        # Use markdown for styling (better than buttons for this UI style)
        file_container.markdown(
            f"""
            <div class="file-item {active_class}" onclick="window.location.search='?file={file_path}'">
                📝 {title_display}
            </div>
            """,
            unsafe_allow_html=True,
        )


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
            index_container = st.container()
            index_container.markdown(
                f"""
                <div class="file-item" onclick="window.location.search='?file={subcategory_data["index"]}'">
                    📄 {subcat_display} Index
                </div>
                """,
                unsafe_allow_html=True,
            )

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

        # Use container and markdown for consistent styling
        file_container = st.container()
        file_container.markdown(
            f"""
            <div class="file-item {active_class}" style="margin-left: 8px;" 
                onclick="window.location.search='?file={subfile_path}'">
                📝 {subtitle_display}
            </div>
            """,
            unsafe_allow_html=True,
        )


def handle_file_selection():
    """Handle file selection via URL parameters or defaults"""
    # Parameter-based navigation
    file_param = st.query_params.get("file")

    if file_param and os.path.exists(file_param):
        st.session_state.selected_file = file_param
    # Default to index.md if no file is selected
    elif not hasattr(st.session_state, "selected_file") or not os.path.exists(
        st.session_state.selected_file
    ):
        st.session_state.selected_file = "index.md"
        # Update the URL to reflect the default selection
        if not file_param:
            st.query_params["file"] = "index.md"

    # Check if the selected file exists
    if not os.path.exists(st.session_state.selected_file):
        st.error(f"File not found: {st.session_state.selected_file}")
        st.session_state.selected_file = "index.md"
        st.query_params["file"] = "index.md"

    return st.session_state.selected_file


def create_breadcrumbs(selected_file_path):
    """Create breadcrumb navigation for the current file"""
    try:
        # Try to make a relative path if possible
        base_path = os.path.abspath(os.path.curdir)
        if os.path.abspath(selected_file_path).startswith(base_path):
            # File is within the project directory
            rel_path = os.path.relpath(selected_file_path, base_path)
            breadcrumb_parts = rel_path.split(os.sep)
        else:
            # File is outside project directory or using absolute path
            breadcrumb_parts = selected_file_path.split(os.sep)
            # Remove empty parts (from leading /)
            breadcrumb_parts = [p for p in breadcrumb_parts if p]
    except ValueError:
        # Fallback if relative path fails
        breadcrumb_parts = selected_file_path.split(os.sep)
        breadcrumb_parts = [p for p in breadcrumb_parts if p]

    if len(breadcrumb_parts) > 0:
        breadcrumb_html = " > ".join(
            [f'<span style="color: #0068c9">{part}</span>' for part in breadcrumb_parts]
        )
        st.markdown(f"<p><small>{breadcrumb_html}</small></p>", unsafe_allow_html=True)


def display_content_tabs(md_content, selected_file_path):
    """Display content in tabs (rendered and source)"""
    tab1, tab2 = st.tabs(["Rendered View", "Source"])

    with tab1:
        # Convert to HTML and process links/images
        html_content = md_to_html(md_content)
        html_content = process_images(html_content, selected_file_path)
        html_content = process_links(html_content, selected_file_path)

        # Display the rendered content
        st.markdown(html_content, unsafe_allow_html=True)

    with tab2:
        # Display the raw markdown
        st.code(md_content, language="markdown")


def display_file_metadata(selected_file_path):
    """Display file metadata like last updated time"""
    mod_time = os.path.getmtime(selected_file_path)
    st.markdown(
        f"<p><small>Last updated: {datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')}</small></p>",
        unsafe_allow_html=True,
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

    # Read and process the selected file
    md_content = read_md_file(selected_file_path)

    # Extract and display the title
    title = extract_title(md_content)
    st.title(title)

    # Create breadcrumbs
    create_breadcrumbs(selected_file_path)

    # Display file metadata
    display_file_metadata(selected_file_path)

    # Display content tabs
    display_content_tabs(md_content, selected_file_path)


if __name__ == "__main__":
    main()
