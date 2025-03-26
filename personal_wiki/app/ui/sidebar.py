import streamlit as st
from personal_wiki.app.utils.file import get_category_from_path
from personal_wiki.app.ui.css import apply_sidebar_css
from personal_wiki.app.ui.theme import show_theme_selector

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
    
    # Add theme selector to the sidebar
    show_theme_selector()
    
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