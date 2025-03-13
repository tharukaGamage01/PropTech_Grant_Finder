import streamlit as st
from search import search_grants
from ranking import rank_results
from utils import load_keywords, modify_keywords

# Sidebar Navigation
st.sidebar.title("Navigation Menu")
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "search"

if st.sidebar.button("Search Grants", key="nav_search", use_container_width=True):
    st.session_state.page = "search"
if st.sidebar.button("Edit Keywords", key="nav_modify", use_container_width=True):
    st.session_state.page = "modify"

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Properties Technologies")

# Load Keywords
file_path = "../data/AI Grant Finding & Writing - Keywords_M2_TG.xlsx"
keyword_list = load_keywords(file_path)


# Search Page
def render_search_page():
    st.title("PropTech Grant Finder")
    user_keyword = st.text_input("Enter a keyword for grant search:", placeholder="e.g., AI, Housing, Renewable Energy")

    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Search", key="search_button", use_container_width=True):
            if user_keyword:
                search_results = search_grants(user_keyword)
                ranked_results = rank_results(search_results, user_keyword, keyword_list)
                st.session_state["ranked_results"] = ranked_results
            else:
                st.warning("Please enter a keyword.")

    if "ranked_results" in st.session_state:
        for result in st.session_state["ranked_results"]:
            st.subheader(result["title"])
            st.write(result["snippet"])
            st.write(f"[Read More]({result['link']})")
            st.markdown("---")


def render_modify_page():
    st.title("✏ Edit Keywords")
    modify_keywords(file_path)


if st.session_state.page == "search":
    render_search_page()
elif st.session_state.page == "modify":
    render_modify_page()
