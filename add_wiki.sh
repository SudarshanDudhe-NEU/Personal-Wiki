#!/bin/bash

# Wiki page creator script for personal-wiki
# Usage: ./add_wiki.sh [category/subcategory] [page-name]

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check for required arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Insufficient arguments${NC}"
    echo -e "Usage: ./add_wiki.sh [category/subcategory] [page-name]"
    echo -e "Example: ./add_wiki.sh technology/ai-ml chatgpt-prompts"
    exit 1
fi

# Get full category path and page name
FULL_CATEGORY=$1
PAGE_NAME=$2

# Parse the category and possible subcategory
if [[ "$FULL_CATEGORY" == */* ]]; then
    # Handle subcategory case
    CATEGORY=$(echo $FULL_CATEGORY | cut -d'/' -f1)
    SUBCATEGORY=$(echo $FULL_CATEGORY | cut -d'/' -f2-)
    FILE_PATH="categories/$FULL_CATEGORY/$PAGE_NAME.md"
    DIRECTORY="categories/$FULL_CATEGORY"
    CATEGORY_INDEX="categories/$CATEGORY.md"
    SUBCATEGORY_INDEX="categories/$FULL_CATEGORY/index.md"
else
    # Handle main category case
    CATEGORY=$FULL_CATEGORY
    SUBCATEGORY=""
    FILE_PATH="categories/$CATEGORY/$PAGE_NAME.md"
    DIRECTORY="categories/$CATEGORY"
    CATEGORY_INDEX="categories/$CATEGORY.md"
    SUBCATEGORY_INDEX=""
fi

TITLE=$(echo "$PAGE_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g' | sed 's/-/ /g')
DATE=$(date +"%Y-%m-%d")
MAIN_INDEX_PATH="index.md"

# Check if main category is valid (basic validation)
valid_categories=("technology" "books" "projects" "notes")
valid_category=0

for valid_cat in "${valid_categories[@]}"; do
    if [ "$CATEGORY" == "$valid_cat" ]; then
        valid_category=1
        break
    fi
done

if [ $valid_category -eq 0 ]; then
    echo -e "${YELLOW}Warning: '$CATEGORY' is not one of the standard categories.${NC}"
    read -p "Do you want to continue with this new category? (y/n): " CREATE_CATEGORY
    if [[ $CREATE_CATEGORY != "y" && $CREATE_CATEGORY != "Y" ]]; then
        echo -e "${BLUE}Exiting without creating file.${NC}"
        exit 0
    fi
    
    # Create new main category
    mkdir -p "categories/$CATEGORY"
    echo -e "# $CATEGORY\n\nThis category contains articles related to $CATEGORY.\n\n## Articles\n" > "categories/$CATEGORY.md"
    echo -e "${GREEN}Created new main category: $CATEGORY${NC}"
fi

# Check if directory exists, if not create it
if [ ! -d "$DIRECTORY" ]; then
    echo -e "${BLUE}Creating directory structure: $DIRECTORY${NC}"
    mkdir -p "$DIRECTORY"
    
    # Create subcategory index if needed
    if [ ! -z "$SUBCATEGORY" ]; then
        # Get the subcategory title from the last part of the path
        SUBCAT_TITLE=$(basename "$SUBCATEGORY" | sed -r 's/(^|-)([a-z])/\U\2/g' | sed 's/-/ /g')
        echo -e "# $SUBCAT_TITLE\n\nArticles related to $SUBCAT_TITLE.\n\n## Articles\n" > "$SUBCATEGORY_INDEX"
        echo -e "${GREEN}Created subcategory index at: $SUBCATEGORY_INDEX${NC}"
    fi
fi

# Check if file already exists
if [ -f "$FILE_PATH" ]; then
    echo -e "${RED}Error: File already exists at $FILE_PATH${NC}"
    exit 1
fi

# Create file with template
cat > "$FILE_PATH" << EOL
# ${TITLE}

Brief introduction about ${TITLE}.

## Background

Context and background information.

## Main Content

Detailed explanation, steps, or information about the topic.

### Subtopic 1

Content for subtopic 1.

### Subtopic 2

Content for subtopic 2.

## Examples

\`\`\`
Example code or usage
\`\`\`

## References

- [Reference 1](https://example.com)
- [Reference 2](https://example.com)

## Last Updated

Date: $DATE
EOL

echo -e "${GREEN}Wiki page created successfully at: $FILE_PATH${NC}"

# Construct relative path for links
if [ ! -z "$SUBCATEGORY" ]; then
    # For subcategory pages, need to adjust the path
    RELATIVE_PATH="./$FULL_CATEGORY/$PAGE_NAME.md"
else
    RELATIVE_PATH="./$CATEGORY/$PAGE_NAME.md"
fi

# Update the category index file
if [ -f "$CATEGORY_INDEX" ]; then
    # Check if the entry already exists to avoid duplicates
    if ! grep -q "\[$TITLE\]($RELATIVE_PATH)" "$CATEGORY_INDEX"; then
        # Add the entry under the Articles section
        sed -i '' '/## Articles/a\
- ['$TITLE']('$RELATIVE_PATH')
' "$CATEGORY_INDEX"
        echo -e "${GREEN}Updated category index at: $CATEGORY_INDEX${NC}"
    fi
fi

# Update subcategory index if applicable
if [ ! -z "$SUBCATEGORY_INDEX" ] && [ -f "$SUBCATEGORY_INDEX" ]; then
    # For subcategory index, use a simpler relative path
    LOCAL_PATH="./$PAGE_NAME.md"
    
    # Check if the entry already exists
    if ! grep -q "\[$TITLE\]($LOCAL_PATH)" "$SUBCATEGORY_INDEX"; then
        # Add the entry under the Articles section
        sed -i '' '/## Articles/a\
- ['$TITLE']('$LOCAL_PATH')
' "$SUBCATEGORY_INDEX"
        echo -e "${GREEN}Updated subcategory index at: $SUBCATEGORY_INDEX${NC}"
    fi
fi

# Update the main index.md with recent updates
if [ -f "$MAIN_INDEX_PATH" ]; then
    # Check if the Recent Updates section exists
    if grep -q "## Recent Updates" "$MAIN_INDEX_PATH"; then
        # Add the new entry at the top of the Recent Updates section
        sed -i '' '/## Recent Updates/a\
- Added ['$TITLE'](./categories/'$FULL_CATEGORY'/'$PAGE_NAME'.md) ('$DATE')
' "$MAIN_INDEX_PATH"
        echo -e "${GREEN}Updated main index with new entry${NC}"
    else
        echo -e "${YELLOW}Warning: Could not find '## Recent Updates' section in $MAIN_INDEX_PATH${NC}"
    fi
fi

# Offer to open the file
read -p "Would you like to open this file now? (y/n): " OPEN_FILE
if [[ $OPEN_FILE == "y" || $OPEN_FILE == "Y" ]]; then
    if command -v code &> /dev/null; then
        code "$FILE_PATH"
    else
        open "$FILE_PATH"
    fi
fi

echo -e "${GREEN}Don't forget to commit your changes!${NC}"
echo -e "git add $FILE_PATH $CATEGORY_INDEX $SUBCATEGORY_INDEX $MAIN_INDEX_PATH"
echo -e "git commit -m \"Add wiki page on ${TITLE}\""
echo -e "git push"