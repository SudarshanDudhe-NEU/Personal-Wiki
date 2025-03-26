import markdown
from bs4 import BeautifulSoup
import base64
import os
from html import escape

def md_to_html(md_content):
    """Convert markdown to HTML with extended features"""
    html = markdown.markdown(
        md_content, 
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
    )
    return html

def extract_title(md_content):
    """Extract title from markdown content"""
    import re
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"

def process_images(html_content, base_path):
    """Process image links to display them properly"""
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

def process_links(html_content, current_file):
    """Process internal links to make them work in the app"""
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
    
    # Process links
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href.startswith('./'):
            # This is a relative link to another wiki file
            target_path = os.path.normpath(os.path.join(os.path.dirname(current_file), href[2:]))
            link['href'] = f"?file={target_path}"
            link['target'] = "_self"  # Ensure the link stays within the app
    
    return str(soup)

def clean_code_blocks(html_content):
    """Clean up code blocks to ensure proper display with special characters"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for pre in soup.find_all('pre'):
        if pre.code:
            code_content = pre.code.get_text()
            new_code = soup.new_tag('code')
            escaped_content = escape(code_content)
            new_code.append(BeautifulSoup(f"<![CDATA[{escaped_content}]]>", 'html.parser'))
            pre.code.replace_with(new_code)
    
    return str(soup)