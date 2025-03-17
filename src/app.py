import streamlit as st
from src.search import search_grants
from src.ranking import rank_results
from src.utils import load_keywords, match_keywords, modify_keywords
import os
import time

st.sidebar.title("Navigation Menu")
st.sidebar.markdown("---")

if "page" not in st.session_state:
    st.session_state.page = "search"

st.session_state.page = st.sidebar.selectbox("Select:", ["Search Grants", "Edit Keywords"], index=0)

st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Properties Technologies")

file_path = "data/AI Grant Finding & Writing - Keywords_M2_TG.xlsx"
if os.path.exists(file_path):
    keyword_list = load_keywords(file_path)
else:
    st.error("Keyword file not found. Please check the file path.")
    keyword_list = []

def show_alert(message, alert_type="info", duration=2):
    alert_container = st.empty()  

    if alert_type == "error":
        alert_container.error(message)
    elif alert_type == "warning":
        alert_container.warning(message)
    elif alert_type == "success":
        alert_container.success(message)
    else:
        alert_container.info(message)

    time.sleep(duration)  
    alert_container.empty() 

def search_grants_action():
    user_input = st.session_state.get("search_input", "").strip()

    if not user_input:
        st.session_state["ranked_results"] = None  
        show_alert("Please enter a keyword", "warning")
        return

    matched_keyword = match_keywords(user_input, keyword_list)  
    if not matched_keyword:
        st.session_state["ranked_results"] = None  
        show_alert("No matching keywords found. Please use relevant keywords.", "error")
        return

    search_query = matched_keyword  
    search_results = search_grants(search_query)

    if search_results:
        ranked_results = rank_results(search_results, [matched_keyword], keyword_list)
        st.session_state["ranked_results"] = ranked_results
    else:
        st.session_state["ranked_results"] = None  
        show_alert("No grants found. Try using a different keyword.", "error")
    
    st.session_state["last_search"] = user_input  

def render_search_page():
    st.markdown("<h1 style='text-align: center;'>PropTech Grant Finder</h1>", unsafe_allow_html=True)

    user_input = st.text_input(
        "Enter a keyword for grant search:",
        placeholder="e.g., AI, Housing, Renewable Energy",
        key="search_input",
        on_change=search_grants_action
    )

    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Search", key="search_button", use_container_width=True):
            st.session_state["ranked_results"] = None  
            st.session_state["last_search"] = st.session_state["search_input"]  
            search_grants_action()

    if "ranked_results" in st.session_state and st.session_state["ranked_results"]:
        st.markdown("### Search Results:")
        st.markdown(
            """
            <style>
            .result-container {
                background-color: #26272f;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                width: 100%;
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

if st.session_state.page == "Search Grants": 
    render_search_page()
elif st.session_state.page == "Edit Keywords":
    modify_keywords(file_path)
