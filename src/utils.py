import pandas as pd
import re
import streamlit as st


def load_keywords(file_path):
    try:
        if not file_path or not file_path.endswith(".xlsx"):
            raise ValueError("Invalid file path or format.")
        df = pd.read_excel(file_path, dtype=str)
        return df["Keywords"].dropna().tolist() if "Keywords" in df.columns else []
    except Exception as e:
        st.error(f"Error loading keywords: {e}")
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
        st.error(f"Error loading categories: {e}")
        return []


def modify_keywords(file_path):
    password = "admin123"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_password = st.text_input("Enter Password:", type="password")
        if st.button("Submit Password"):
            if user_password == password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password! Try again.")
        return

    if not file_path or not file_path.endswith(".xlsx"):
        st.error("Invalid file path or format.")
        return

    categories = load_categories(file_path)
    if not categories:
        st.error("No categories found in the file.")
        return

    action = st.selectbox("Choose Action", ["Add", "Remove"])
    category = st.selectbox("Select Category", categories)
    new_keyword = st.text_input("Enter Keyword:", value=st.session_state.get("new_keyword", "")).strip()

    if st.button("Submit", key="submit_keyword"):
        if not new_keyword:
            st.error("Please enter a keyword before submitting.")
        else:
            st.session_state.show_warning = True
            st.session_state.new_keyword = new_keyword
            st.rerun()

    if st.session_state.get("show_warning", False):
        st.warning("Are you sure you want to apply these changes?")

        if st.button("OK", key="confirm_changes"):
            try:
                df = pd.read_excel(file_path, dtype=str)
                if "Category" not in df.columns or "Keywords" not in df.columns:
                    st.error("Invalid file format. Please ensure 'Category' and 'Keywords' columns exist.")
                    return

                if action == "Add":
                    if df[(df["Category"] == category) & (df["Keywords"] == new_keyword)].empty:
                        new_row = pd.DataFrame({"Category": [category], "Keywords": [new_keyword]})
                        df = pd.concat([df, new_row], ignore_index=True)
                    else:
                        st.warning("Keyword already exists in the selected category.")
                        return
                elif action == "Remove":
                    if df[(df["Category"] == category) & (df["Keywords"] == new_keyword)].empty:
                        st.warning("Keyword not found in the selected category.")
                        return
                    df = df[~((df["Category"] == category) & (df["Keywords"] == new_keyword))]

                df.to_excel(file_path, index=False)
                st.success("Updated Successfully!")

                st.session_state.show_warning = False
                st.session_state.new_keyword = ""
                st.rerun()
            except Exception as e:
                st.error(f"Error updating the file: {e}")
