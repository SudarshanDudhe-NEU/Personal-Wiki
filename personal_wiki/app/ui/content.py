import streamlit as st
import os
import datetime
import re
from pathlib import Path
from personal_wiki.app.utils.markdown import md_to_html, process_images, process_links, clean_code_blocks, extract_title
from personal_wiki.app.utils.file import read_md_file

def handle_file_selection():
    """Handle file selection via URL parameters or defaults"""
    # Parameter-based navigation
    query_params = st.experimental_get_query_params()
    file_param = query_params.get("file")

    if file_param and os.path.exists(file_param[0]):
        st.session_state.selected_file = file_param[0]
    # Default to index.md if no file is selected
    elif not hasattr(st.session_state, "selected_file") or not os.path.exists(
        st.session_state.selected_file
    ):
        st.session_state.selected_file = "index.md"
        # Update the URL to reflect the default selection
        if not file_param:
            st.experimental_set_query_params(file="index.md")

    # Check if the selected file exists
    if not os.path.exists(st.session_state.selected_file):
        st.error(f"File not found: {st.session_state.selected_file}")
        st.session_state.selected_file = "index.md"
        st.experimental_set_query_params(file="index.md")

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
        # Extract and store code blocks
        code_blocks = []
        content_parts = []
        
        # Match fenced code blocks with language specifier
        pattern = r"```([a-zA-Z0-9_+-]*)\n(.*?)```"
        
        # Process the markdown content
        last_end = 0
        for match in re.finditer(pattern, md_content, re.DOTALL):
            # Add text before this code block
            if match.start() > last_end:
                content_parts.append(md_content[last_end:match.start()])
                
            # Add a placeholder for the code block
            lang = match.group(1).strip()
            code = match.group(2)
            code_blocks.append((lang, code))
            content_parts.append(f"CODE_BLOCK_{len(code_blocks) - 1}")
            
            last_end = match.end()
        
        # Add any remaining content
        if last_end < len(md_content):
            content_parts.append(md_content[last_end:])
            
        # Join all non-code parts
        processed_md = "".join(content_parts)
        
        # Convert to HTML and process links/images
        html_content = md_to_html(processed_md)
        html_content = process_images(html_content, selected_file_path)
        html_content = process_links(html_content, selected_file_path)
        
        # Split by code block placeholders
        html_parts = html_content.split("CODE_BLOCK_")
        
        # Display first part
        if html_parts[0].strip():
            st.markdown(html_parts[0], unsafe_allow_html=True)
            
        # Display each code block followed by subsequent content
        for i, part in enumerate(html_parts[1:], 0):
            # Find the block number
            block_num = i
            
            # Display the code block using Streamlit's code element
            lang, code = code_blocks[block_num]
            st.code(code, language=lang if lang else None)
            
            # Find where the actual content starts
            content_start = part.find(">") + 1 if ">" in part else 0
            
            # Display the rest of this section if any
            if part[content_start:].strip():
                st.markdown(part[content_start:], unsafe_allow_html=True)
    
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

def display_content(selected_file_path):
    """Display the main content area with the selected markdown file"""
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