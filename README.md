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

## Accessing Your Wiki

### Local Access

1. **Using VS Code** (Recommended):
   - Open the repository in VS Code
   - Use the built-in Markdown preview (Command+Shift+V on Mac)
   - Navigate through files using links in the preview

2. **Using a Markdown Viewer**:
   - Install a dedicated viewer like [Typora](https://typora.io/) or [Obsidian](https://obsidian.md/)
   - Open your wiki directory in the application
   - Navigate using the links between pages

3. **Terminal-based Options**:
   ```bash
   # Option 1: Using glow (recommended terminal viewer)
   brew install glow
   glow categories/technology/docker-basics.md
   
   # Option 2: Using bat with syntax highlighting
   brew install bat
   bat categories/technology/docker-basics.md
   
   # Option 3: If you prefer Python-based tools (in a virtual env)
   python3 -m venv venv
   source venv/bin/activate
   pip install grip
   grip categories/technology/docker-basics.md
   # This starts a local server at http://localhost:6419
   ```

### Browser-based Access

1. **Local HTTP Server**:
   ```bash
   # Start a simple HTTP server in your wiki directory
   python3 -m http.server
   
   # Then visit in your browser:
   # http://localhost:8000/
   ```

2. **GitHub Pages** (recommended for remote access):
   - Enable GitHub Pages in your repository settings
   - Your wiki will be available at `https://yourusername.github.io/personal-wiki/`
   - Changes are automatically deployed when you push to the repository

3. **Setting up GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Set source to your main branch
   - Choose root folder (/) as the source directory
   - Wait a few minutes for deployment
   - GitHub will provide the URL where your site is hosted

### Mobile Access

- Access through GitHub's mobile app
- Use the GitHub Pages site from any mobile browser
- Consider using working copies (iOS) or MGit (Android) for Git access on mobile

### Wiki Structure

Your current wiki structure:
```
.
├── README.md
├── _config.yml
├── add_wiki.sh
├── categories/
│   ├── books.md
│   ├── notes.md
│   ├── projects.md
│   ├── technology/
│   │   ├── docker-basics.md
│   │   └── llama3-local-setup.md
│   └── technology.md
├── index.md
├── requirements.txt
└── templates/
    └── note-template.md
```

Navigate through your wiki by starting at `index.md` and following the category links.

## Git Workflow

Always pull before making changes to avoid conflicts:

```bash
git pull
# Make your changes
git add .
git commit -m "Your descriptive message"
git push
```
