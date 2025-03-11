import pandas as pd
import re
import streamlit as st


def load_keywords(file_path):
    df = pd.read_excel(file_path) if file_path else pd.DataFrame()
    return df["Keywords"].tolist() if "Keywords" in df.columns else []


def extract_keywords(user_input):
    return re.findall(r'\b\w+\b', user_input.lower())


def modify_keywords(file_path):
    password = "admin123"
    user_password = st.text_input("Enter Password:", type="password")
    submit_password = st.button("Submit Password")

    if submit_password and user_password == password:
        st.success("Access Granted!")
        action = st.selectbox("Choose Action", ["Add", "Remove"])
        category = st.text_input("Enter Category:")
        new_keyword = st.text_input("Enter Keyword:")
        confirm_edit = st.checkbox("Confirm Edit")

        if st.button("Submit") and confirm_edit:
            df = pd.read_excel(file_path)
            if action == "Add" and new_keyword:
                df = df.append({category: new_keyword}, ignore_index=True)
            elif action == "Remove" and new_keyword in df[category].values:
                df = df[df[category] != new_keyword]
            df.to_excel(file_path, index=False)
            st.success("Updated Successfully!")
    elif submit_password:
        st.error("Incorrect password! Try again.")
