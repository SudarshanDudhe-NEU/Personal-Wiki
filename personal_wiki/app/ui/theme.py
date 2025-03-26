import streamlit as st
import toml
import os

# Available themes
THEMES = {
    "Light": {
        "primaryColor": "#0068c9",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#31333F",
        "font": "sans serif"
    },
    "Dark": {
        "primaryColor": "#4da6ff",
        "backgroundColor": "#0e1117",
        "secondaryBackgroundColor": "#262730",
        "textColor": "#fafafa",
        "font": "sans serif"
    },
    "Forest": {
        "primaryColor": "#2e7d32",
        "backgroundColor": "#f8f9fa",
        "secondaryBackgroundColor": "#e8f5e9",
        "textColor": "#212529",
        "font": "serif"
    },
    "Oceanic": {
        "primaryColor": "#03a9f4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#e1f5fe",
        "textColor": "#01579b",
        "font": "sans serif"
    },
    "Vintage": {
        "primaryColor": "#795548",
        "backgroundColor": "#f9f5eb",
        "secondaryBackgroundColor": "#e0d9c8",
        "textColor": "#4e342e",
        "font": "serif"
    }
}

def save_theme_config(theme_name):
    """Save selected theme to config.toml"""
    if theme_name not in THEMES:
        return False
    
    # Make sure .streamlit directory exists
    streamlit_dir = os.path.join(os.path.expanduser("~"), ".streamlit")
    os.makedirs(streamlit_dir, exist_ok=True)
    config_path = os.path.join(streamlit_dir, "config.toml")
    
    # Create or update config file
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = toml.load(f)
        except Exception:
            config = {}
    
    # Update theme configuration
    config["theme"] = THEMES[theme_name]
    
    # Write configuration
    with open(config_path, "w") as f:
        toml.dump(config, f)
    
    return True

def show_theme_selector():
    """Display theme selector in sidebar"""
    with st.sidebar.expander("🎨 Theme Settings", expanded=False):
        theme_options = list(THEMES.keys())
        
        # Default to Light theme
        selected_theme = st.selectbox(
            "Select theme:",
            theme_options,
            index=0,
            key="theme_selector"
        )
        
        if st.button("Apply Theme", key="apply_theme"):
            save_theme_config(selected_theme)
            st.success(f"Theme updated to {selected_theme}! Refresh to see changes.")
            st.markdown(
                """
                <script>
                    setTimeout(function() {
                        window.location.reload();
                    }, 1500);
                </script>
                """, 
                unsafe_allow_html=True
            )