#!/bin/bash

# add_wiki.sh - Script to add new wiki pages to personal wiki
# Usage: ./add_wiki.sh <category> <page-name>

set -e

# Configuration
WIKI_ROOT="$(pwd)"
CATEGORIES_DIR="$WIKI_ROOT/personal_wiki/categories"
TEMPLATES_DIR="$WIKI_ROOT/templates"
MAIN_INDEX="$WIKI_ROOT/index.md"
DEFAULT_TEMPLATE="$TEMPLATES_DIR/page_template.md"
STANDARD_CATEGORIES=("technology" "books" "projects" "notes")

# Function to convert kebab-case to Title Case
to_title_case() {
    # More robust implementation for macOS
    local words=$(echo "$1" | tr '-' ' ')
    local result=""
    for word in $words; do
        first_char=$(echo "${word:0:1}" | tr '[:lower:]' '[:upper:]')
        rest_chars=$(echo "${word:1}")
        result="$result $first_char$rest_chars"
    done
    echo "${result:1}"  # Remove leading space
}

# Function to check if a value is in an array
in_array() {
    local needle="$1"
    for element in "${@:2}"; do
        if [[ "$element" == "$needle" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to update recent updates in the main index
update_main_index() {
    local title="$1"
    local file_path="$2"
    local relative_path="${file_path#$WIKI_ROOT/}"
    
    # Check if the recent updates section exists
    if ! grep -q "## Recent Updates" "$MAIN_INDEX"; then
        echo -e "\n## Recent Updates\n" >> "$MAIN_INDEX"
    fi
    
    # Add the entry at the top of the recent updates section
    current_date=$(date +"%Y-%m-%d")
    sed -i '' "/## Recent Updates/a\\
- $current_date: [$title]($relative_path)" "$MAIN_INDEX"
    
    echo "Updated main index with link to new page"
}

# Function to update category index
update_category_index() {
    local category_dir="$1"
    local category_name="$2"
    local page_title="$3"
    local page_file="$4"
    
    local index_file="$category_dir.md"
    local category_title=$(to_title_case "$category_name")
    local relative_path="$(basename "$page_file")"
    
    # Create category index if it doesn't exist
    if [[ ! -f "$index_file" ]]; then
        echo "# $category_title" > "$index_file"
        echo -e "\nDocumentation and notes related to $category_title.\n" >> "$index_file"
        echo "## Pages" >> "$index_file"
    fi
    
    # Check if the Pages section exists
    if ! grep -q "## Pages" "$index_file"; then
        echo -e "\n## Pages" >> "$index_file"
    fi
    
    # Add the entry to the Pages section
    sed -i '' "/## Pages/a\\
- [$page_title]($relative_path)" "$index_file"
    
    echo "Updated category index at $index_file"
}

# Validate arguments
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <category> <page-name>"
    echo "Example: $0 technology docker-basics"
    echo "Example with subcategory: $0 technology/ai-ml chatgpt-prompts"
    exit 1
fi

CATEGORY="$1"
PAGE_NAME="$2"
MAIN_CATEGORY=$(echo "$CATEGORY" | cut -d'/' -f1)

# Validate main category
if ! in_array "$MAIN_CATEGORY" "${STANDARD_CATEGORIES[@]}"; then
    read -p "Warning: '$MAIN_CATEGORY' is not a standard category. Continue? [y/N] " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Aborted. Standard categories are: ${STANDARD_CATEGORIES[*]}"
        exit 1
    fi
fi

# Determine file paths
if [[ "$CATEGORY" == */* ]]; then
    # Handle subcategory
    SUB_CATEGORY=$(echo "$CATEGORY" | cut -d'/' -f2)
    CATEGORY_DIR="$CATEGORIES_DIR/$MAIN_CATEGORY/$SUB_CATEGORY"
    PARENT_DIR="$CATEGORIES_DIR/$MAIN_CATEGORY"
else
    # Handle main category
    CATEGORY_DIR="$CATEGORIES_DIR/$CATEGORY"
    PARENT_DIR="$CATEGORIES_DIR"
fi

# Create directories if they don't exist
mkdir -p "$CATEGORY_DIR"

# Set file paths
FILE_PATH="$CATEGORY_DIR/$PAGE_NAME.md"
PAGE_TITLE=$(to_title_case "$PAGE_NAME")

# Check if file already exists
if [[ -f "$FILE_PATH" ]]; then
    read -p "Warning: '$FILE_PATH' already exists. Overwrite? [y/N] " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create the file from template
if [[ -f "$DEFAULT_TEMPLATE" ]]; then
    cp "$DEFAULT_TEMPLATE" "$FILE_PATH"
    # Replace template variables
    sed -i '' "s/{{TITLE}}/$PAGE_TITLE/g" "$FILE_PATH"
    sed -i '' "s/{{DATE}}/$(date +"%Y-%m-%d")/g" "$FILE_PATH"
else
    # Create minimal file if template doesn't exist
    echo "# $PAGE_TITLE" > "$FILE_PATH"
    echo -e "\nCreated: $(date +"%Y-%m-%d")\n" >> "$FILE_PATH"
    echo "## Overview" >> "$FILE_PATH"
    echo -e "\nAdd your content here.\n" >> "$FILE_PATH"
fi

echo "Created new wiki page at $FILE_PATH"

# Update indexes
if [[ "$CATEGORY" == */* ]]; then
    # Update subcategory index
    SUB_CATEGORY=$(echo "$CATEGORY" | cut -d'/' -f2)
    update_category_index "$CATEGORY_DIR" "$SUB_CATEGORY" "$PAGE_TITLE" "$FILE_PATH"
    
    # Also update parent category index if needed
    PARENT_INDEX="$PARENT_DIR.md"
    if [[ -f "$PARENT_INDEX" ]]; then
        SUB_CATEGORY_TITLE=$(to_title_case "$SUB_CATEGORY")
        # Add subcategory link if not already present
        if ! grep -q "$SUB_CATEGORY_TITLE" "$PARENT_INDEX"; then
            if ! grep -q "## Subcategories" "$PARENT_INDEX"; then
                echo -e "\n## Subcategories" >> "$PARENT_INDEX"
            fi
            RELATIVE_PATH="$MAIN_CATEGORY/$SUB_CATEGORY.md"
            sed -i '' "/## Subcategories/a\\
- [$SUB_CATEGORY_TITLE]($RELATIVE_PATH)" "$PARENT_INDEX"
        fi
        echo "Updated parent category index at $PARENT_INDEX"
    fi
else
    # Update main category index
    update_category_index "$CATEGORY_DIR" "$CATEGORY" "$PAGE_TITLE" "$FILE_PATH"
fi

# Update main index
update_main_index "$PAGE_TITLE" "$FILE_PATH"

echo "Successfully added new wiki page: $PAGE_TITLE"

# Offer to open the file
read -p "Would you like to open the new file for editing? [Y/n] " open_file
if [[ "$open_file" != "n" && "$open_file" != "N" ]]; then
    if command -v code &> /dev/null; then
        code "$FILE_PATH"
    elif command -v open &> /dev/null; then
        open "$FILE_PATH"
    else
        echo "No suitable editor found. Please open $FILE_PATH manually."
    fi
fi