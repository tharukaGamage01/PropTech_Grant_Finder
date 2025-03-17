import pandas as pd
import re
import streamlit as st
from fuzzywuzzy import fuzz, process
import time
import os
from dotenv import load_dotenv
load_dotenv()

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

def load_keywords(file_path):
    try:
        if not file_path or not file_path.endswith(".xlsx"):
            raise ValueError("Invalid file path or format.")
        df = pd.read_excel(file_path, dtype=str)
        return df["Keywords"].dropna().tolist() if "Keywords" in df.columns else []
    except Exception as e:
        show_alert(f"Error loading keywords: {e}", "error")
        return []

def extract_keywords(user_input):
    if not user_input or not isinstance(user_input, str):
        return []
    return re.findall(r'\b\w+\b', user_input.lower())

def load_categories(file_path):
    try:
        if not file_path or not file_path.endswith(".xlsx"):
            raise ValueError("Invalid file path or format.")
        df = pd.read_excel(file_path, dtype=str)
        return df["Category"].dropna().unique().tolist() if "Category" in df.columns else []
    except Exception as e:
        show_alert(f"Error loading categories: {e}", "error")
        return []

def match_keywords(word, keyword_list):
    if not keyword_list:
        return None  

    result = process.extractOne(word, keyword_list, scorer=fuzz.partial_ratio)
    return result[0] if result else None  

def modify_keywords(file_path):
   
    password = os.getenv("PASSWORD")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_password = st.text_input("Enter Password:", type="password")
        if st.button("Submit Password"):
            if user_password == password:
                st.session_state.authenticated = True
                show_alert("Login successful!", "success") 
                st.rerun()
            else:
                show_alert("Incorrect password! Try again.", "error")
        return

    if not file_path or not file_path.endswith(".xlsx"):
        show_alert("Invalid file path or format.", "error")
        return

    categories = load_categories(file_path)
    if not categories:
        show_alert("No categories found in the file.", "error")
        return

    action = st.selectbox("Choose Action", ["Add", "Remove"])
    category = st.selectbox("Select Category", categories)
    new_keyword = st.text_input("Enter Keyword:", value=st.session_state.get("new_keyword", "")).strip()

    if st.button("Submit", key="submit_keyword"):
        if not new_keyword:
            show_alert("Please enter a keyword before submitting.", "error")
        else:
            st.session_state.new_keyword = new_keyword
            try:
                df = pd.read_excel(file_path, dtype=str)
                if "Category" not in df.columns or "Keywords" not in df.columns:
                    show_alert("Invalid file format. Please ensure 'Category' and 'Keywords' columns exist.", "error")
                    return

                if action == "Add":
                    if df[(df["Category"] == category) & (df["Keywords"] == new_keyword)].empty:
                        new_row = pd.DataFrame({"Category": [category], "Keywords": [new_keyword]})
                        df = pd.concat([df, new_row], ignore_index=True)
                        show_alert("Keyword added successfully!", "success")
                    else:
                        show_alert("Keyword already exists in the selected category.", "warning")
                        return
                elif action == "Remove":
                    if df[(df["Category"] == category) & (df["Keywords"] == new_keyword)].empty:
                        show_alert("Keyword not found in the selected category.", "warning")
                        return
                    df = df[~((df["Category"] == category) & (df["Keywords"] == new_keyword))]
                    show_alert("Keyword removed successfully!", "success")

                df.to_excel(file_path, index=False)
                st.session_state.new_keyword = ""
                st.rerun()
            except Exception as e:
                show_alert(f"Error updating the file: {e}", "error")
