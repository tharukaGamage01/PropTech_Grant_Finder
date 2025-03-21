import pytest
import requests
import streamlit as st
from unittest.mock import patch
from src.search import (
    search_google_grants,
    search_grants_gov,
    search_uk_gov_grants,
    fallback_grant_sources
)


@patch("requests.get")
@patch("streamlit.secrets.get", side_effect=lambda key, default=None: "fake_key" if key == "GOOGLE_API_KEY" else "fake_id")
def test_search_google_grants_valid(mock_secrets_get, mock_get):
    mock_response = {
        "items": [
            {"title": "AI Research Grant", "link": "https://example.com/ai-grant", "snippet": "Funding for AI projects."}
        ]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    results = search_google_grants("AI funding")
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]["title"] == "AI Research Grant"

@patch("streamlit.secrets.get", side_effect=lambda key, default=None: None)
def test_search_google_grants_missing_keys(mock_secrets_get):
    results = search_google_grants("AI funding")
    assert results == []


@patch("requests.get")
def test_search_grants_gov(mock_get):
    mock_response = {
        "opportunityDetails": [
            {"title": "Tech Startup Grant", "synopsisURL": "https://grants.gov/tech-startup", "agencyName": "US Gov"}
        ]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    results = search_grants_gov()
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]["title"] == "Tech Startup Grant"


@patch("requests.get")
def test_search_uk_gov_grants(mock_get):
    mock_response = {
        "details": {
            "business_finance_support": [
                {"title": "UK AI Grant", "web_url": "/ai-funding", "description": "Support for AI businesses."}
            ]
        }
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    results = search_uk_gov_grants()
    assert isinstance(results, list)
    assert len(results) > 0
    assert "UK AI Grant" in results[0]["title"]


def test_fallback_grants():
    results = fallback_grant_sources()
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
