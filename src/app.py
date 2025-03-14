import streamlit as st
from search import search_grants
from ranking import rank_results
from utils import load_keywords, modify_keywords
import os

# Sidebar Navigation
st.sidebar.title("Navigation Menu")
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "search"  # Set default page to 'search'

if st.sidebar.button("Search Grants", key="nav_search", use_container_width=True):
    st.session_state.page = "search"
if st.sidebar.button("Edit Keywords", key="nav_modify", use_container_width=True):
    st.session_state.page = "modify"

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Properties Technologies")

# Load Keywords
file_path = "../data/AI Grant Finding & Writing - Keywords_M2_TG.xlsx"
if os.path.exists(file_path):
    keyword_list = load_keywords(file_path)
else:
    st.error("Keyword file not found. Please check the file path.")
    keyword_list = []

# Function to execute search
def search_grants_action():
    user_keyword = st.session_state.get("search_input", "").strip()
    if user_keyword:
        search_results = search_grants(user_keyword)
        if search_results:
            ranked_results = rank_results(search_results, user_keyword, keyword_list)
            st.session_state["ranked_results"] = ranked_results
        else:
            st.warning("No results found for the entered keyword.")
    else:
        st.warning("Please enter a valid keyword.")

# Function to render search page
def render_search_page():
    st.markdown("<h1 style='text-align: center;'>PropTech Grant Finder</h1>", unsafe_allow_html=True)

    user_keyword = st.text_input(
        "Enter a keyword for grant search:",
        placeholder="e.g., AI, Housing, Renewable Energy",
        key="search_input",
        on_change=search_grants_action
    )

    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Search", key="search_button", use_container_width=True):
            search_grants_action()

    if "ranked_results" in st.session_state and st.session_state["ranked_results"]:
        st.markdown("### Search Results:")

        st.markdown(
            """
            <style>
            .result-container {
                background-color: #2c2c2c;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
            </style>
            """, unsafe_allow_html=True
        )

        for result in st.session_state["ranked_results"]:
            st.markdown(f"""
            <div class="result-container">
                <h3>{result["title"]}</h3>
                <p>{result["snippet"]}</p>
                <a href="{result['link']}" target="_blank">Read More</a>
            </div>
            """, unsafe_allow_html=True)
    elif "ranked_results" in st.session_state:
        st.info("No grants found. Try using a different keyword.")

# Page Navigation Logic
if st.session_state.page == "search":
    render_search_page()
elif st.session_state.page == "modify":
    modify_keywords(file_path)  # Only call modify_keywords when needed
