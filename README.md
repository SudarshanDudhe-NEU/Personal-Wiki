````markdown
# Personal Wiki

My knowledge base for organizing information, notes, and references.

## Structure

- index.md - Main entry point and table of contents
- personal_wiki - Main package containing app and content
  - `app/` - Streamlit application code (modular structure)
  - `categories/` - Topic-specific content organized by category
    - `technology/` - Technology-related articles
      - `programming-languages/` - Programming languages subfolder
      - `web-development/` - Web development subfolder
    - `books/` - Book summaries and reviews
    - `projects/` - Project documentation
    - `notes/` - General notes and research
- templates - Templates for new content
- run_wiki.py - Entry point for running the Streamlit viewer

## How to Use

This wiki is maintained using Git and formatted in Markdown.

### Adding New Wiki Pages

You can add new wiki pages using the provided script for consistency.

#### Using the Script

1. Make the script executable (first time only):

   ```bash
   chmod +x add_wiki.sh
   ```
````

2. Run the script with category and page name:

   ```bash
   ./add_wiki.sh technology docker-basics
   ```

3. This will:

   - Create a new page with a standard template at docker-basics.md
   - Update the category index file with a link to your new page
   - Add the new page to the Recent Updates section in the main index
   - Offer to open the new file for immediate editing

4. Edit the file and add your content

5. Commit your changes:
   ```bash
   git add personal_wiki/categories/technology/docker-basics.md personal_wiki/categories/technology.md index.md
   git commit -m "Add wiki page on Docker Basics"
   git push
   ```

### Using the Script with Subcategories

The script supports both main categories and subcategories:

```bash
# Adding to a main category
./add_wiki.sh technology docker-basics

# Adding to a subcategory
./add_wiki.sh technology/ai-ml chatgpt-prompts
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
   glow personal_wiki/categories/technology/docker-basics.md

   # Option 2: Using bat with syntax highlighting
   brew install bat
   bat personal_wiki/categories/technology/docker-basics.md

   # Option 3: If you prefer Python-based tools (in a virtual env)
   python3 -m venv venv
   source venv/bin/activate
   pip install grip
   grip personal_wiki/categories/technology/docker-basics.md
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

## Git Workflow

Always pull before making changes to avoid conflicts:

```bash
git pull
# Make your changes
git add .
git commit -m "Your descriptive message"
git push
```

## Visualizing Your Wiki with Streamlit

This wiki includes a modular Streamlit application for a beautiful, interactive visualization of your content.

### Setup

1. Install the required dependencies:

   ```bash
   pip install -r personal_wiki/requirements.txt
   ```

2. Run the Streamlit application:

   ```bash
   streamlit run run_wiki.py
   ```

3. The application will open in your browser at `http://localhost:8501`

### Application Architecture

The Streamlit viewer is organized in a modular structure:

- run_wiki.py - Entry point that initializes the application
- app - Core application code
  - `main.py` - Main application logic and page setup
  - `ui/` - User interface components
    - `sidebar.py` - Navigation sidebar
    - `content.py` - Content display and rendering
    - `css.py` - Custom styling
    - `theme.py` - Theme management
  - `utils/` - Utility functions
    - `file.py` - File system operations
    - `markdown.py` - Markdown processing
    - `search.py` - Search functionality

### Features

- **Interactive Navigation**: Browse through categories and files using the enhanced sidebar
- **Beautiful Rendering**: Clean, styled display of your Markdown content
- **Source View**: Toggle between rendered view and source markdown
- **Breadcrumb Navigation**: See your current location in the wiki
- **Responsive Design**: Works well on desktop and mobile devices
- **Active State Highlighting**: Clear visual indicators for current category and page
- **Search Functionality**: Quickly find content across your wiki
- **Code Syntax Highlighting**: Beautiful display of code blocks with language detection

### Customizing the Theme

The Streamlit wiki viewer supports multiple themes:

1. **Built-in Themes**:

   - Choose from Light, Dark, Forest, Oceanic, and Vintage themes
   - Use the Theme Settings expander in the sidebar

2. **Custom Themes**:
   - Edit config.toml directly to create custom themes
   - Add your own color schemes and font selections

Example theme configuration:

```toml
[theme]
primaryColor = "#0068c9"        # Main accent color
backgroundColor = "#ffffff"     # Main content background
secondaryBackgroundColor = "#f0f2f6"  # Sidebar background
textColor = "#31333F"           # Text color
font = "sans serif"             # Font family
```
