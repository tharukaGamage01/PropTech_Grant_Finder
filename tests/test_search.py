import pytest
from src.search import search_grants
import streamlit as st
from unittest.mock import patch

def test_search_grants_missing_keys():
   
    with patch.object(st, "secrets", {}):
        with pytest.raises(ValueError, match="Missing API keys"):
            search_grants("AI grants")

def test_search_grants_empty_query():
   
    with patch.object(st, "secrets", {"GOOGLE_API_KEY": "test_key", "SEARCH_ENGINE_ID": "test_id"}):
        with pytest.raises(ValueError, match="Search query cannot be empty."):
            search_grants("")
