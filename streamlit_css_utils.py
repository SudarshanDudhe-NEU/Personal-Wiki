import streamlit as st


# Custom CSS to make the wiki look nicer
def local_css():
    st.markdown(
        """
    <style>
        .main {
            padding: 0rem 1rem;
        }
        .stMarkdown h1 {
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #f0f2f6;
        }
        .stMarkdown h2 {
            padding-bottom: 0.3rem;
            border-bottom: 1px solid #f0f2f6;
            margin-top: 1.5rem;
        }
        .stMarkdown pre {
            border-radius: 5px;
        }
        .stMarkdown img {
            max-width: 100%;
            height: auto;
        }
        .stMarkdown table {
            width: 100%;
            border-collapse: collapse;
        }
        .stMarkdown th, .stMarkdown td {
            border: 1px solid #f0f2f6;
            padding: 8px;
            text-align: left;
        }
        .stMarkdown tr:nth-child(even) {
            background-color: #f0f2f6;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: auto;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }
        .stTabs [aria-selected="true"] {
            background-color: #e0e2e6 !important;
            border-bottom: 3px solid #0068c9 !important;
        }
        .sidebar-category {
            margin-left: 10px;
        }
        .sidebar-file {
            margin-left: 20px;
        }
        .sidebar-subcategory {
            margin-left: 30px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def apply_sidebar_css():
    """Apply custom CSS for improved sidebar appearance"""
    st.markdown("""
    <style>
        /* Sidebar header styling */
        .css-1lcbmhc.e1fqkh3o0, .css-1aehpvj.e1fqkh3o0 {
            padding-top: 1rem !important;
            padding-bottom: 0.5rem !important;
        }
        
        /* Button styling */
        .nav-button {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .nav-button:hover {
            background-color: rgba(151, 166, 195, 0.15);
        }
        
        .nav-icon {
            margin-right: 8px;
            font-size: 1.2em;
        }
        
        .nav-label {
            flex-grow: 1;
        }
        
        /* Home button specific styling */
        .home-button {
            background-color: rgba(151, 166, 195, 0.1);
            margin-bottom: 12px;
        }
        
        /* Active category styling */
        .active-category {
            border-left: 3px solid #0068c9;
            padding-left: 9px !important;
            background-color: rgba(0, 104, 201, 0.1);
        }
        
        /* Category item styling */
        .category-item {
            transition: all 0.2s ease;
            border-left: 3px solid transparent;
            padding-left: 12px;
        }
        
        /* File item styling */
        .file-item {
            padding-left: 24px;
            margin: 4px 0;
            display: block;
            color: #444;
            text-decoration: none;
            transition: all 0.2s ease;
            border-radius: 4px;
            padding: 6px 12px 6px 24px;
        }
        
        .file-item:hover {
            background-color: rgba(151, 166, 195, 0.15);
            padding-left: 26px;
        }
        
        .active-file {
            background-color: rgba(0, 104, 201, 0.1);
            font-weight: 500;
        }
        
        /* Subcategory styling */
        .subcategory-label {
            margin-left: 15px;
            margin-top: 10px;
            font-weight: 500;
            display: flex;
            align-items: center;
        }
        
        /* Footer styling */
        .sidebar-footer {
            text-align: center;
            color: #888;
            font-size: 0.8em;
            padding: 10px 0;
        }
        
        /* Mobile responsiveness */
        .mobile-notice {
            display: none;
            text-align: center;
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 4px;
            margin-top: 20px;
        }
        
        .sidebar-note {
            font-size: 0.85em;
            color: #888;
            font-style: italic;
        }
        
        /* Responsive design for mobile */
        @media (max-width: 768px) {
            .mobile-notice {
                display: block;
            }
            
            .nav-button, .file-item {
                padding: 10px 12px; /* Larger touch targets for mobile */
            }
            
            [data-testid="stSidebar"] {
                min-width: 250px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)