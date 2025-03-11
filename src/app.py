import streamlit as st
from search import search_grants
from ranking import rank_results
from utils import load_keywords


st.sidebar.title("Navigation")


def render_navigation():
    if st.sidebar.button("Search Grants", use_container_width=True):
        st.session_state["page"] = "search"
    if st.sidebar.button("Edit Excel", use_container_width=True):
        st.session_state["page"] = "modify"


if "page" not in st.session_state:
    st.session_state["page"] = "search"

render_navigation()

# File Path Handling
file_path = "../data/AI Grant Finding & Writing - Keywords_M2_TG.xlsx"
keyword_list = load_keywords(file_path)

if st.session_state["page"] == "search":
    st.title("AI Grant Finder")
    user_keyword = st.text_input("Enter a keyword for grant search:")
    search_button = st.button("Search")

    if user_keyword and search_button:
        search_results = search_grants(user_keyword)
        ranked_results = rank_results(search_results, user_keyword, keyword_list)
        st.session_state["ranked_results"] = ranked_results

    if "ranked_results" in st.session_state:
        for result in st.session_state["ranked_results"]:
            st.subheader(result["title"])
            st.write(result["snippet"])
            st.write(f"[Read More]({result['link']})")

elif st.session_state["page"] == "modify":
    from utils import modify_keywords

    st.subheader("Modify Keywords")
    modify_keywords(file_path)
