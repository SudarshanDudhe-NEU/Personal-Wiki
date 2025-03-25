# Personal Wiki

My knowledge base for organizing information, notes, and references.

## Structure

- `index.md` - Main entry point and table of contents
- `categories/` - Topic-specific content organized by category

## How to Use

This wiki is maintained using Git and formatted in Markdown.

### Adding New Wiki Pages

You can add new wiki pages using the provided script for consistency.

#### Using the Script

1. Make the script executable (first time only):
   ```bash
   chmod +x add_wiki.sh
   ```

2. Run the script with category and page name:
   ```bash
   ./add_wiki.sh technology docker-basics
   ```

3. This will:
   - Create a new page with a standard template at `categories/technology/docker-basics.md`
   - Update the category index file with a link to your new page
   - Add the new page to the Recent Updates section in the main index
   - Offer to open the new file for immediate editing

4. Edit the file and add your content

5. Commit your changes:
   ```bash
   git add categories/technology/docker-basics.md categories/technology.md index.md
   git commit -m "Add wiki page on Docker Basics"
   git push
   ```

#### Supported Categories

The standard categories are:
- technology
- books
- projects
- notes

You can create new categories, but the script will prompt for confirmation.

#### Features

- **Automatic Updates**: The script automatically updates index files
- **Duplicate Prevention**: Checks for existing files to prevent overwrites
- **Category Validation**: Validates categories against standard options
- **Title Formatting**: Converts kebab-case to Title Case automatically

## Git Workflow

Always pull before making changes to avoid conflicts:

```bash
git pull
# Make your changes
git add .
git commit -m "Your descriptive message"
git push
```
