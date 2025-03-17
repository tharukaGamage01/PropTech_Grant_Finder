import pytest
import os
from src.search import search_grants

@pytest.fixture(autouse=True)
def set_secrets_file(monkeypatch):
 
    monkeypatch.setenv("STREAMLIT_SECRETS_FILE", "tests/.streamlit/secrets.toml")

def test_search_grants_valid_query():
   
    result = search_grants("AI grants")
    assert result is not None  
