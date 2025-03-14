import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest


# def test_search_ui():
#     at = AppTest("main.py")
#     at.run()
#
#     assert at.text_input[0].label == "Enter a keyword for grant search:"
#
#     at.text_input[0].set_value("AI Funding")
#     at.button[0].click()
#
#     assert "Search Results:" in at.markdown[0].value
