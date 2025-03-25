#!/bin/bash

# Wiki page creator script for personal-wiki
# Usage: ./add_wiki.sh [category] [page-name]

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Check for required arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Insufficient arguments${NC}"
    echo -e "Usage: ./add_wiki.sh [category] [page-name]"
    echo -e "Example: ./add_wiki.sh technology docker-basics"
    exit 1
fi

CATEGORY=$1
PAGE_NAME=$2
TITLE=$(echo "$PAGE_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g' | sed 's/-/ /g')
DATE=$(date +"%Y-%m-%d")
FILE_PATH="categories/$CATEGORY/$PAGE_NAME.md"
DIRECTORY="categories/$CATEGORY"
INDEX_PATH="index.md"
CATEGORY_INDEX="categories/$CATEGORY.md"

# Check if category is valid (basic validation)
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
fi

# Check if category directory exists, if not create it
if [ ! -d "$DIRECTORY" ]; then
    echo -e "${BLUE}Creating new category directory: $DIRECTORY${NC}"
    mkdir -p "$DIRECTORY"
    
    # If creating a new category, also create its index file
    echo -e "# $CATEGORY" > $CATEGORY_INDEX
    echo -e "\nThis category contains articles related to $CATEGORY.\n" >> $CATEGORY_INDEX
    echo -e "## Articles\n" >> $CATEGORY_INDEX
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

# Update the category index file if it exists
if [ -f "$CATEGORY_INDEX" ]; then
    # Check if the entry already exists to avoid duplicates
    if ! grep -q "\[$TITLE\](./$CATEGORY/$PAGE_NAME.md)" "$CATEGORY_INDEX"; then
        # Add the entry under the Articles section
        sed -i '' '/## Articles/a\
- ['$TITLE'](./'$CATEGORY'/'$PAGE_NAME'.md)
' "$CATEGORY_INDEX"
        echo -e "${GREEN}Updated category index at: $CATEGORY_INDEX${NC}"
    fi
fi

# Update the main index.md with recent updates
if [ -f "$INDEX_PATH" ]; then
    # Check if the Recent Updates section exists
    if grep -q "## Recent Updates" "$INDEX_PATH"; then
        # Add the new entry at the top of the Recent Updates section
        sed -i '' '/## Recent Updates/a\
- Added ['$TITLE'](./categories/'$CATEGORY'/'$PAGE_NAME'.md) ('$DATE')
' "$INDEX_PATH"
        echo -e "${GREEN}Updated main index with new entry${NC}"
    else
        echo -e "${YELLOW}Warning: Could not find '## Recent Updates' section in $INDEX_PATH${NC}"
    fi
else
    echo -e "${RED}Error: Main index file $INDEX_PATH not found${NC}"
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
echo -e "git add $FILE_PATH $CATEGORY_INDEX $INDEX_PATH"
echo -e "git commit -m \"Add wiki page on ${TITLE}\""
echo -e "git push"