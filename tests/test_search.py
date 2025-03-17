import pytest
import os
import shutil
from src.search import search_grants


@pytest.fixture(autouse=True)
def set_secrets_file(tmpdir):
   
    streamlit_dir = tmpdir.mkdir(".streamlit")
    dummy_secrets_path = os.path.join("tests", ".streamlit", "secrets.toml")
    shutil.copy(dummy_secrets_path, streamlit_dir)
    os.chdir(tmpdir)


def test_search_grants_valid_query():
   
    result = search_grants("AI grants")
    assert result is not None  


def test_search_grants_missing_keys(monkeypatch):
   
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("SEARCH_ENGINE_ID", raising=False)
    with pytest.raises(ValueError, match="Missing API keys"):
        search_grants("AI grants")


def test_search_grants_empty_query():
  
    with pytest.raises(ValueError, match="Search query cannot be empty."):
        search_grants("")
