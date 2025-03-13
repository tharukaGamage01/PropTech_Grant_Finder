import pandas as pd
import re
import streamlit as st


def load_keywords(file_path):
    df = pd.read_excel(file_path) if file_path else pd.DataFrame()
    return df["Keywords"].tolist() if "Keywords" in df.columns else []


def extract_keywords(user_input):
    return re.findall(r'\b\w+\b', user_input.lower())


def load_categories(file_path):
    df = pd.read_excel(file_path) if file_path else pd.DataFrame()
    return df["Category"].dropna().unique().tolist() if "Category" in df.columns else []


def modify_keywords(file_path):
    password = "admin123"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_password = st.text_input("Enter Password:", type="password")
        if st.button("Submit Password", key="submit_password"):
            if user_password == password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password! Try again.")
        return

    categories = load_categories(file_path)
    if not categories:
        st.error("No categories found in the file.")
        return

    action = st.selectbox("Choose Action", ["Add", "Remove"])
    category = st.selectbox("Select Category", categories)

    new_keyword = st.text_input("Enter Keyword:", value=st.session_state.get("new_keyword", ""))

    if st.button("Submit", key="submit_keyword"):
        if not new_keyword:
            st.error("Please enter a keyword before submitting.")
        else:
            st.session_state.show_warning = True
            st.session_state.new_keyword = new_keyword
            st.rerun()

    if st.session_state.get("show_warning", False):
        st.warning("Are you sure you want to apply these changes?")

        # Ensure unique keys for "OK" buttons
        if st.button("OK", key="confirm_changes"):
            df = pd.read_excel(file_path)

            if action == "Add":
                new_row = pd.DataFrame({"Category": [category], "Keywords": [st.session_state.new_keyword]})
                df = pd.concat([df, new_row], ignore_index=True)
            elif action == "Remove":
                df = df[~((df["Category"] == category) & (df["Keywords"] == st.session_state.new_keyword))]

            df.to_excel(file_path, index=False)

            st.success("Updated Successfully!")

            st.session_state.show_warning = False
            st.session_state.new_keyword = ""
            st.rerun()


file_paths = "../data/AI Grant Finding & Writing - Keywords_M2_TG.xlsx"
modify_keywords(file_paths)
