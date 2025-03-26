import os
import glob
import re
import markdown
import base64
from bs4 import BeautifulSoup


# Parse markdown to HTML with extended features
def md_to_html(md_content):
    # Use the fenced_code and codehilite extensions for better code block handling
    html = markdown.markdown(
        md_content, 
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'  # Add this to handle line breaks
        ]
    )
    return html


# Get all markdown files in the wiki with their paths
def get_md_files():
    """Get all markdown files in the wiki with their paths"""
    md_files = {}
    categories = get_main_categories()

    for category in categories:
        category_name = os.path.basename(category).replace(".md", "")
        md_files[category_name] = {
            "path": category,
            "files": get_category_files(category_name),
        }

        # Process subcategories
        subcategories = get_subcategories(category_name)
        md_files[category_name]["subcategories"] = process_subcategories(
            category_name, subcategories
        )

    return md_files


def get_main_categories():
    """Get all main category markdown files"""
    return [f for f in glob.glob("categories/*.md") if not "index.md" in f]


def get_category_files(category_name):
    """Get all files directly in a category"""
    files = {}
    category_dir = os.path.join("categories", category_name)

    if os.path.isdir(category_dir):
        subfiles = glob.glob(f"{category_dir}/*.md")
        for subfile in subfiles:
            file_name = os.path.basename(subfile).replace(".md", "")
            files[file_name] = subfile

    return files


def get_subcategories(category_name):
    """Get all subcategories in a category"""
    category_dir = os.path.join("categories", category_name)
    if os.path.isdir(category_dir):
        return [
            d
            for d in os.listdir(category_dir)
            if os.path.isdir(os.path.join(category_dir, d))
        ]
    return []


def process_subcategories(category_name, subcategories):
    """Process all subcategories and their files"""
    result = {}

    for subcategory in subcategories:
        result[subcategory] = {}
        subcategory_path = os.path.join("categories", category_name, subcategory)

        # Get the index file for the subcategory
        index_file = os.path.join(subcategory_path, "index.md")
        if os.path.exists(index_file):
            result[subcategory]["index"] = index_file

        # Get files in the subcategory
        result[subcategory]["files"] = get_subcategory_files(subcategory_path)

    return result


def get_subcategory_files(subcategory_path):
    """Get all files in a subcategory"""
    files = {}

    subcat_files = [
        f for f in glob.glob(f"{subcategory_path}/*.md") if not "index.md" in f
    ]

    for subcat_file in subcat_files:
        file_name = os.path.basename(subcat_file).replace(".md", "")
        files[file_name] = subcat_file

    return files


# Extract title from markdown content
def extract_title(md_content):
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"


# Read markdown file content
def read_md_file(file_path):
    """Read markdown file content"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


# Process image links to display them properly
def process_images(html_content, base_path):
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("./"):
            img_path = os.path.join(os.path.dirname(base_path), src[2:])
            if os.path.exists(img_path):
                with open(img_path, "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode()
                    img["src"] = f"data:image/png;base64,{encoded}"
    return str(soup)


# Process internal links to make them work in the app
def process_links(html_content, current_file):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Fix for code blocks - ensure they're properly displayed
    for pre in soup.find_all('pre'):
        # For each pre tag (which contains code blocks)
        if pre.code:
            # Get the text content directly without processing
            code_text = pre.code.get_text()
            # Create a new code element with the original text
            new_code = soup.new_tag('code')
            new_code.string = code_text
            # Replace the old code with the new one
            pre.code.replace_with(new_code)
    
    # Process links as before
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href.startswith('./'):
            # This is a relative link to another wiki file
            target_path = os.path.normpath(os.path.join(os.path.dirname(current_file), href[2:]))
            link['href'] = f"?file={target_path}"
            link['target'] = "_self"  # Ensure the link stays within the app
    
    return str(soup)

# Additional function to clean up code blocks before display
def clean_code_blocks(html_content):
    """Clean up code blocks to ensure proper display with special characters"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all code blocks
    for pre in soup.find_all('pre'):
        if pre.code:
            # Get the raw code content
            code_content = pre.code.get_text()
            
            # Create a new code element
            new_code = soup.new_tag('code')
            
            # Escape HTML entities
            from html import escape
            escaped_content = escape(code_content)
            
            # Set the escaped content directly
            new_code.append(BeautifulSoup(f"<![CDATA[{escaped_content}]]>", 'html.parser'))
            
            # Replace the old code element
            pre.code.replace_with(new_code)
    
    return str(soup)

def get_category_from_path(file_path):
    """Extract category name from file path"""
    if not file_path or file_path == "index.md":
        return ""

    parts = file_path.split(os.sep)
    if len(parts) > 1 and parts[0] == "categories":
        if len(parts) > 2:
            return parts[1]  # Return the category name
    return ""