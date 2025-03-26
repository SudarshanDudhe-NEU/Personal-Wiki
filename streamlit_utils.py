import streamlit as st
import os
import markdown
import glob
from bs4 import BeautifulSoup
import re
import base64


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


# Parse markdown to HTML with extended features
def md_to_html(md_content):
    html = markdown.markdown(
        md_content,
        extensions=[
            "markdown.extensions.tables",
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
        ],
    )
    return html


# Get all markdown files in the wiki with their paths
def get_md_files():
    md_files = {}

    # Main categories
    categories = [f for f in glob.glob("categories/*.md") if not "index.md" in f]

    for category in categories:
        category_name = os.path.basename(category).replace(".md", "")
        md_files[category_name] = {}
        md_files[category_name]["path"] = category
        md_files[category_name]["files"] = {}

        # Get sub-files in this category
        category_dir = os.path.join("categories", category_name)
        if os.path.isdir(category_dir):
            subfiles = glob.glob(f"{category_dir}/*.md")
            for subfile in subfiles:
                file_name = os.path.basename(subfile).replace(".md", "")
                md_files[category_name]["files"][file_name] = subfile

            # Check for subcategories
            subcategories = [
                d
                for d in os.listdir(category_dir)
                if os.path.isdir(os.path.join(category_dir, d))
            ]

            md_files[category_name]["subcategories"] = {}

            for subcategory in subcategories:
                md_files[category_name]["subcategories"][subcategory] = {}
                subcategory_path = os.path.join(category_dir, subcategory)

                # Get the index file for the subcategory
                index_file = os.path.join(subcategory_path, "index.md")
                if os.path.exists(index_file):
                    md_files[category_name]["subcategories"][subcategory][
                        "index"
                    ] = index_file

                # Get files in the subcategory
                subcat_files = [
                    f
                    for f in glob.glob(f"{subcategory_path}/*.md")
                    if not "index.md" in f
                ]
                md_files[category_name]["subcategories"][subcategory]["files"] = {}

                for subcat_file in subcat_files:
                    file_name = os.path.basename(subcat_file).replace(".md", "")
                    md_files[category_name]["subcategories"][subcategory]["files"][
                        file_name
                    ] = subcat_file

    return md_files


# Extract title from markdown content
def extract_title(md_content):
    match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"


# Read markdown file content
def read_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


# Process image links to display them properly
def process_images(html_content, base_path):
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("./"):
            img_path = os.path.join(os.path.dirname(base_path), src[2:])
            if os.path.exists(img_path):
                with open(img_path, "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode()
                    img["src"] = f"data:image/png;base64,{encoded}"
    return str(soup)


# Process internal links to make them work in the app
def process_links(html_content, current_file):
    soup = BeautifulSoup(html_content, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.startswith("./"):
            # This is a relative link to another wiki file
            target_path = os.path.normpath(
                os.path.join(os.path.dirname(current_file), href[2:])
            )
            link["href"] = f"?file={target_path}"
            link["target"] = "_self"  # Ensure the link stays within the app
    return str(soup)
