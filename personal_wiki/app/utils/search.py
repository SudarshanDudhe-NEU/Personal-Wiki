import os
import re
from personal_wiki.app.utils.file import read_md_file

def search_wiki_content(search_term, md_files):
    """Search markdown files for content matching search term"""
    results = []
    term_lower = search_term.lower()
    
    # Search function to process each file
    def search_file(file_path, title=None):
        try:
            content = read_md_file(file_path).lower()
            if term_lower in content:
                # If no title provided, extract it from content
                if not title:
                    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE | re.IGNORECASE)
                    if match:
                        title = match.group(1)
                    else:
                        title = os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
                
                results.append({
                    'path': file_path,
                    'title': title,
                    'snippet': extract_snippet(content, term_lower)
                })
        except Exception as e:
            print(f"Error searching file {file_path}: {e}")
    
    # Process each category
    for category_name, category_data in md_files.items():
        # Search category main file
        search_file(category_data['path'], category_name.capitalize())
        
        # Search files in category
        for file_name, file_path in category_data['files'].items():
            search_file(file_path)
        
        # Search subcategories
        if 'subcategories' in category_data:
            for subcategory_name, subcategory_data in category_data['subcategories'].items():
                # Search subcategory index
                if 'index' in subcategory_data:
                    search_file(subcategory_data['index'], f"{subcategory_name.capitalize()} Index")
                
                # Search files in subcategory
                for subfile_name, subfile_path in subcategory_data.get('files', {}).items():
                    search_file(subfile_path)
    
    return results

def extract_snippet(content, search_term, chars=50):
    """Extract a snippet of text around the search term"""
    position = content.find(search_term)
    if position == -1:
        return ""
    
    start = max(0, position - chars)
    end = min(len(content), position + len(search_term) + chars)
    
    # Get the snippet
    snippet = content[start:end]
    
    # Add ellipsis if needed
    if start > 0:
        snippet = f"...{snippet}"
    if end < len(content):
        snippet = f"{snippet}..."
    
    return snippet