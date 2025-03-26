import streamlit as st
import os
import datetime

from pathlib import Path
from streamlit_utils import *

# Set page configuration
st.set_page_config(
    page_title="Personal Wiki Viewer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Main application
def main():
    local_css()

    # Get wiki structure
    md_files = get_md_files()

    # Sidebar title
    st.sidebar.title("📚 Wiki Navigation")

    # Add index link
    if st.sidebar.button("📄 Home/Index", key="home"):
        st.session_state.selected_file = "index.md"

    # Categories in sidebar
    for category_name, category_data in md_files.items():
        category_title = category_name.capitalize()

        # Category expander
        with st.sidebar.expander(f"📁 {category_title}"):
            # Category main page
            if st.button(f"📄 {category_title} overview", key=f"cat_{category_name}"):
                st.session_state.selected_file = category_data["path"]

            # Files directly in the category
            for file_name, file_path in category_data["files"].items():
                title_display = file_name.replace("-", " ").title()
                if st.button(
                    f"📝 {title_display}", key=f"file_{category_name}_{file_name}"
                ):
                    st.session_state.selected_file = file_path

            # Subcategories if they exist
            if "subcategories" in category_data and category_data["subcategories"]:
                st.markdown("#### Subcategories")

                for subcategory_name, subcategory_data in category_data[
                    "subcategories"
                ].items():
                    subcat_display = subcategory_name.replace("-", " ").title()

                    # Display subcategory as a section with proper formatting instead of nested expander
                    st.markdown(
                        f"<div style='margin-left: 15px; margin-top: 10px;'><b>📁 {subcat_display}</b></div>",
                        unsafe_allow_html=True,
                    )

                    # Subcategory index if it exists
                    if "index" in subcategory_data:
                        if st.button(
                            f"📄 {subcat_display} Index",
                            key=f"subcat_index_{category_name}_{subcategory_name}",
                        ):
                            st.session_state.selected_file = subcategory_data["index"]

                    # Files in the subcategory
                    for subfile_name, subfile_path in subcategory_data.get(
                        "files", {}
                    ).items():
                        subtitle_display = subfile_name.replace("-", " ").title()
                        col1, col2 = st.columns([0.2, 3])
                        with col2:
                            if st.button(
                                f"📝 {subtitle_display}",
                                key=f"subfile_{category_name}_{subcategory_name}_{subfile_name}",
                            ):
                                st.session_state.selected_file = subfile_path

    # Parameter-based navigation
    file_param = st.query_params.get("file")
    if file_param and os.path.exists(file_param):
        st.session_state.selected_file = file_param

    # Default to index.md if no file is selected
    if not hasattr(st.session_state, "selected_file"):
        st.session_state.selected_file = "index.md"

    # Check if the selected file exists
    if not os.path.exists(st.session_state.selected_file):
        st.error(f"File not found: {st.session_state.selected_file}")
        st.session_state.selected_file = "index.md"

    # Display the selected file
    selected_file_path = st.session_state.selected_file
    md_content = read_md_file(selected_file_path)

    # Extract the title for the page
    title = extract_title(md_content)
    st.title(title)

    # Show file path as breadcrumbs
    # Fix the path issue by using os.path operations instead of Path.relative_to
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

    # Display last updated time
    mod_time = os.path.getmtime(selected_file_path)
    st.markdown(
        f"<p><small>Last updated: {datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M')}</small></p>",
        unsafe_allow_html=True,
    )

    # Tabs for viewing content
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


if __name__ == "__main__":
    main()
