#!/bin/bash

# add_index_files.sh - Script to add index.md files to empty folders
# Usage: ./add_index_files.sh

set -e

WIKI_ROOT="$(pwd)"
CATEGORIES_DIR="$WIKI_ROOT/personal_wiki/categories"

# Function to convert kebab-case or snake_case to Title Case
to_title_case() {
    local name=$(echo "$1" | tr '-_' '  ')
    local result=""
    for word in $name; do
        first_char=$(echo "${word:0:1}" | tr '[:lower:]' '[:upper:]')
        rest_chars=$(echo "${word:1}")
        result="$result $first_char$rest_chars"
    done
    echo "${result:1}"  # Remove leading space
}

# Function to create an index.md file in a directory
create_index_file() {
    local dir="$1"
    local index_file="$dir/index.md"
    
    # Skip if index.md already exists
    if [[ -f "$index_file" ]]; then
        echo "Index file already exists in $dir"
        return 0
    fi
    
    # Get the directory name and convert to title case
    local dir_name=$(basename "$dir")
    local title=$(to_title_case "$dir_name")
    
    # Get the parent directory name for context
    local parent_dir=$(basename "$(dirname "$dir")")
    local parent_title=$(to_title_case "$parent_dir")
    
    echo "Creating index for '$title' in '$parent_title' category"
    
    # Create the index.md file
    cat > "$index_file" << EOF
# ${title}

Documentation and resources related to ${title} in the ${parent_title} category.

## Overview

This section contains information, tutorials, and references about ${title}.

## Pages

*No pages yet. Add content using the \`add_wiki.sh\` script.*

EOF
    
    # Add subcategories section if this is a main category
    if [[ "$parent_dir" == "categories" ]]; then
        cat >> "$index_file" << EOF

## Subcategories

*No subcategories yet.*
EOF
    fi
    
    echo "Created index file in $dir"
}

# Function to fix an existing but incorrectly formatted index file
fix_index_file() {
    local dir="$1"
    local index_file="$dir/index.md"
    
    # Only process if file exists and is empty or missing title
    if [[ ! -f "$index_file" ]]; then
        return 0
    fi
    
    # Check if first line is empty or just "#"
    local first_line=$(head -n 1 "$index_file")
    if [[ "$first_line" == "#" || "$first_line" == "# " ]]; then
        echo "Fixing incorrectly formatted index file in $dir"
        
        # Get the directory name and convert to title case
        local dir_name=$(basename "$dir")
        local title=$(to_title_case "$dir_name")
        
        # Get the parent directory name for context
        local parent_dir=$(basename "$(dirname "$dir")")
        local parent_title=$(to_title_case "$parent_dir")
        
        # Create a temporary file with the correct content
        local temp_file="${index_file}.tmp"
        
        cat > "$temp_file" << EOF
# ${title}

Documentation and resources related to ${title} in the ${parent_title} category.

## Overview

This section contains information, tutorials, and references about ${title}.

## Pages

*No pages yet. Add content using the \`add_wiki.sh\` script.*

EOF
        
        # Add subcategories section if this is a main category
        if [[ "$parent_dir" == "categories" ]]; then
            cat >> "$temp_file" << EOF

## Subcategories

*No subcategories yet.*
EOF
        fi
        
        # Replace the original file
        mv "$temp_file" "$index_file"
        echo "Fixed index file in $dir"
    fi
}

# Process all directories
echo "Searching for directories without proper index.md files..."

find "$CATEGORIES_DIR" -type d | while read -r dir; do
    # Skip the root categories directory
    if [[ "$dir" == "$CATEGORIES_DIR" ]]; then
        continue
    fi
    
    # Check if this directory has no index.md
    if [[ ! -f "$dir/index.md" ]]; then
        create_index_file "$dir"
    else
        # Check and fix existing but incorrectly formatted index files
        fix_index_file "$dir"
    fi
done

echo "Done! All directories now have properly formatted index.md files."