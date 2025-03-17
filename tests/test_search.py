import pytest
from src.search import search_grants
import os


def test_search_grants_missing_keys(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("SEARCH_ENGINE_ID", raising=False)

    with pytest.raises(ValueError, match="Missing API keys"):
        search_grants("AI grants")


def test_search_grants_empty_query():
    with pytest.raises(ValueError, match="Search query cannot be empty."):
        search_grants("")
